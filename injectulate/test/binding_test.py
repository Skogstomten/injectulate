from abc import ABCMeta

from .. import Container
from .fixtures import clear_bindings


class AbstractClass(metaclass=ABCMeta):
    pass


class Implementation(AbstractClass):
    pass


def test_can_setup_specific_class_bindings():
    target = Container()
    target.bind(AbstractClass).to(Implementation)

    result = target.get(AbstractClass)

    assert isinstance(result, Implementation)


def test_can_bind_to_factory_method():
    target = Container()
    target.bind(AbstractClass).to(lambda _: Implementation())

    result = target.get(AbstractClass)

    assert isinstance(result, Implementation)
