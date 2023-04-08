from injectulate import inject, Container


class SimpleClass:
    pass


class ClassWithDependency:
    def __init__(self, dependency=inject(SimpleClass)):
        self.dependency = dependency


def test_can_create_class_with_dependency():
    target = Container()
    result = target.get(ClassWithDependency)
    assert isinstance(result, ClassWithDependency)
    assert isinstance(result.dependency, SimpleClass)
