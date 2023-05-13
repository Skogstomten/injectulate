from inspect import signature, Signature, Parameter, isclass, isfunction
from typing import Sequence, Dict, Type, TypeVar, Callable, Any
from abc import ABC, abstractmethod
from .errors import TypeAnnotationError


T = TypeVar("T")


class BindingDefinition(ABC):
    @abstractmethod
    def resolve(self, container: "Container"):
        ...


class TypeBindingDefinition(BindingDefinition):
    def __init__(self, cls: Type):
        super().__init__()
        self.cls = cls

    def resolve(self, container: "Container"):
        return self.cls(*_Resolver(signature(self.cls.__init__), container, self.cls).resolve())


class MethodBindingDefinition(BindingDefinition):
    def __init__(self, func: Callable[["Container"], Any]):
        super().__init__()
        self.func = func

    def resolve(self, container: "Container"):
        return self.func(container)


class BindingContext:
    def __init__(self, cls: Type, builder: "Builder"):
        self.bind_this = cls
        self.builder = builder

    def to(self, bind_to: Type | Callable) -> "Builder":
        if isclass(bind_to):
            self.builder.binding_definitions[self.bind_this] = TypeBindingDefinition(bind_to)
        elif isfunction(bind_to):
            self.builder.binding_definitions[self.bind_this] = MethodBindingDefinition(bind_to)
        return self.builder


class Builder:
    def __init__(self):
        super().__init__()
        self.binding_definitions: Dict[Type, BindingDefinition] = {}

    def build(self) -> "Container":
        return Container(self.binding_definitions)

    def bind(self, cls: Type) -> BindingContext:
        return BindingContext(cls, self)


class _Resolver:
    def __init__(self, sig: Signature, container: "Container", resolution_type: Type):
        self.sig = sig
        self.container = container
        self.resolution_type = resolution_type

    def resolve(self) -> Sequence:
        resolved_arguments = []
        for parameter in self.sig.parameters.values():
            match parameter:
                case Parameter(name="self") | Parameter(name="args") | Parameter(name="kwargs"):
                    continue
                case Parameter() as p if p.annotation in self.container.binding_definitions:
                    resolved_arguments.append(
                        self.container.binding_definitions[parameter.annotation].resolve(self.container)
                    )
                case Parameter(annotation=Parameter.empty):
                    raise TypeAnnotationError(
                        "Parameter '{}' of type '{}' is missing type annotation and can not be resolved.".format(
                            parameter.name, self.resolution_type
                        )
                    )
                case Parameter() as p if p.annotation == Container:
                    resolved_arguments.append(self.container)
                case _:
                    resolved_arguments.append(
                        parameter.annotation(
                            *_Resolver(
                                signature(parameter.annotation.__init__), self.container, parameter.annotation
                            ).resolve()
                        )
                    )
        return resolved_arguments


class Container:
    def __init__(self, binding_definitions: Dict[Type, BindingDefinition] | None = None):
        self.binding_definitions = binding_definitions or {}

    def get(self, cls: T, *args, **kwargs) -> T:
        """
        Get instance of type.

        :param cls: Type of requested instance.
        :param args:
        :param kwargs:
        :return: Instance of type cls
        """
        if cls == Container:
            return self
        if cls in self.binding_definitions:
            return self.binding_definitions[cls].resolve(self)

        return cls(*_Resolver(signature(cls.__init__), self, cls).resolve(), *args, **kwargs)
