from typing import Type, Dict, Callable

from .singleton import Singleton


class _Bindings(metaclass=Singleton):
    def __init__(self):
        self._bindings: Dict[Type, Type] = {}

    def add_binding(self, bind_this: Type, to_this: Type) -> None:
        self._bindings[bind_this] = to_this

    def contains(self, type_to_check: Type) -> bool:
        return type_to_check in self._bindings

    def get_factory(self, type_to_get_factory_for: Type) -> Callable:
        return self._bindings[type_to_get_factory_for]


class _BindingContext:
    def __init__(self, bind_this: Type, bindings: _Bindings):
        self._bind_this: Type = bind_this
        self._bindings: _Bindings = bindings

    def to(self, bind_to: Type) -> None:
        self._bindings.add_binding(self._bind_this, bind_to)


class Container(metaclass=Singleton):
    def __init__(self):
        self._bindings = _Bindings()

    def get(self, type_to_create: Type, *args, **kwargs):
        if self._bindings.contains(type_to_create):
            return self._bindings.get_factory(type_to_create)(*args, **kwargs)
        return type_to_create(*args, **kwargs)

    def bind(self, bind_this) -> _BindingContext:
        if self._bindings.contains(bind_this):
            raise KeyError(f"Binding already exists for type {bind_this}")
        return _BindingContext(bind_this, self._bindings)
