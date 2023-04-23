from inspect import signature, Signature, Parameter
from typing import Sequence, Dict, Type, TypeVar


class BindingDefinition:
    def __init__(self, cls: Type):
        self.cls = cls

    def resolve(self, container: "Container"):
        return self.cls(*_Resolver(signature(self.cls.__init__), container).resolve())


class BindingContext:
    def __init__(self, cls: Type, builder: "Builder"):
        self.bind_this = cls
        self.builder = builder

    def to(self, cls: Type) -> "Builder":
        self.builder.binding_definitions[self.bind_this] = BindingDefinition(cls)
        return self.builder


class Builder:
    def __init__(self):
        self.binding_definitions: Dict[Type, BindingDefinition] = {}

    def build(self) -> "Container":
        return Container(self.binding_definitions)

    def bind(self, cls: Type) -> BindingContext:
        return BindingContext(cls, self)


class _Resolver:
    def __init__(self, sig: Signature, container: "Container"):
        self._sig = sig
        self._container = container

    def resolve(self) -> Sequence:
        resolved_arguments = []
        for parameter in self._sig.parameters.values():
            match parameter:
                case Parameter(name="self") | Parameter(name="args") | Parameter(name="kwargs"):
                    continue
                case Parameter() as p if p.annotation in self._container.binding_definitions:
                    resolved_arguments.append(
                        self._container.binding_definitions[parameter.annotation].resolve(self._container)
                    )
                case Parameter() as p if p.annotation == Container:
                    resolved_arguments.append(self._container)
                case _:
                    resolved_arguments.append(
                        parameter.annotation(
                            *_Resolver(signature(parameter.annotation.__init__), self._container).resolve()
                        )
                    )
        return resolved_arguments


T = TypeVar("T")


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

        return cls(*_Resolver(signature(cls.__init__), self).resolve(), *args, **kwargs)
