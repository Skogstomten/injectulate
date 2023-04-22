from typing import Iterable
from inspect import signature, Signature, Parameter


class _Resolver:
    def __init__(self, sig: Signature, container: "Container"):
        self._sig = sig
        self._container = container

    def resolve(self) -> Iterable:
        resolved_arguments = []
        for parameter in self._sig.parameters.values():
            if parameter.annotation == Container:
                resolved_arguments.append(self._container)
                continue

            match parameter:
                case Parameter(name="self") | Parameter(name="args") | Parameter(name="kwargs"):
                    continue
                case _:
                    resolved_arguments.append(
                        parameter.annotation(
                            *_Resolver(signature(parameter.annotation.__init__), self._container).resolve()
                        )
                    )
        return resolved_arguments


class Container:
    def get(self, cls: type, *args, **kwargs):
        """
        Get instance of type.

        :param cls: Type of requested instance.
        :param args:
        :param kwargs:
        :return: Instance of type cls
        """
        if cls == Container:
            return self

        return cls(*_Resolver(signature(cls.__init__), self).resolve(), *args, **kwargs)
