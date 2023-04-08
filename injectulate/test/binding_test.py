from abc import ABCMeta

from .. import Container


class AbstractClass(metaclass=ABCMeta):
    pass


class Implementation(AbstractClass):
    pass


def test_can_setup_specific_class_bindings():
    target = Container()
    target.bind(AbstractClass).to(Implementation)

    result = target.get(AbstractClass)

    assert isinstance(result, Implementation)
