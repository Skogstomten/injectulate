from abc import ABC

from pytest import fixture, raises

from .. import Container, Builder
from ..errors import TypeAnnotationError


@fixture
def target(builder) -> Container:
    return builder.build()


@fixture
def builder() -> Builder:
    return Builder()


def test_can_get_simple_class(target):
    class SimpleClass:
        pass

    assert isinstance(target.get(SimpleClass), SimpleClass)


def test_can_get_instance_of_self(target):
    result = target.get(Container)
    assert isinstance(result, Container)
    assert result == target


def test_can_get_class_with_dependency_on_container(target):
    class ClassWithDependencyOnContainer:
        def __init__(self, container: Container):
            self.container = container

    result = target.get(ClassWithDependencyOnContainer)
    assert isinstance(result, ClassWithDependencyOnContainer)
    assert result.container == target


def test_can_get_class_with_other_class_dependency(target):
    class SimpleClass:
        pass

    class ClassWithDependency:
        def __init__(self, dependency: SimpleClass):
            self.dependency = dependency

    result = target.get(ClassWithDependency)
    assert isinstance(result, ClassWithDependency)
    assert isinstance(result.dependency, SimpleClass)


def test_can_get_implementation_of_abstract_class(builder):
    class AbstractClass(ABC):
        pass

    class Implementation(AbstractClass):
        pass

    builder.bind(AbstractClass).to(Implementation)
    target = builder.build()
    assert isinstance(target.get(AbstractClass), Implementation)


def test_class_with_dependency_missing_type_throws_type_annotation_error(target):
    class SomeClass:
        def __init__(self, dependency):
            self.dependency = dependency

    with raises(TypeAnnotationError):
        target.get(SomeClass)


def test_can_bind_to_factory_method(builder):
    class AbstractClass(ABC):
        pass

    class Implementation(AbstractClass):
        pass

    builder.bind(AbstractClass).to(lambda c: Implementation())
    target = builder.build()
    assert isinstance(target.get(AbstractClass), Implementation)
