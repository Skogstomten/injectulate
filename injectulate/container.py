from typing import Type, Dict, Callable, Tuple
from enum import Enum

from .singleton import Singleton


class _BindingType(Enum):
    bind_to_type = "bind_to_type"
    bind_to_method = "bind_to_method"


class Scope(Enum):
    transient = "transient"


class _Bindings(metaclass=Singleton):
    def __init__(self):
        self._bindings: Dict[Type, Tuple[_BindingType, Scope, Type | Callable]] = {}

    def add_binding(self, bind_this: Type, to_this: Type | Callable) -> None:
        self._bindings[bind_this] = (
            _BindingType.bind_to_type if isinstance(to_this, type) else _BindingType.bind_to_method,
            Scope.transient,
            to_this
        )

    def contains(self, type_to_check: Type) -> bool:
        return type_to_check in self._bindings

    def get(self, type_to_get_factory_for: Type) -> Tuple[_BindingType, Scope, Type | Callable]:
        return self._bindings[type_to_get_factory_for]

    def clear(self):
        self._bindings.clear()


class _BindingContext:
    def __init__(self, bind_this: Type, bindings: _Bindings):
        self._bind_this: Type = bind_this
        self._bindings: _Bindings = bindings

    def to(self, bind_to: Type | Callable) -> None:
        self._bindings.add_binding(self._bind_this, bind_to)


class Container(metaclass=Singleton):
    def __init__(self):
        self._bindings = _Bindings()

    def get(self, type_to_create: Type, *args, **kwargs):
        if self._bindings.contains(type_to_create):
            binding_type, _, target = self._bindings.get(type_to_create)
            if binding_type == _BindingType.bind_to_method:
                return target(self)
            return target(*args, **kwargs)
        return type_to_create(*args, **kwargs)

    def bind(self, bind_this) -> _BindingContext:
        if self._bindings.contains(bind_this):
            raise KeyError(f"Binding already exists for type {bind_this}")
        return _BindingContext(bind_this, self._bindings)

    def clear(self):
        self._bindings.clear()
