from pytest import fixture

from .. import Container


@fixture
def target():
    return Container()


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
