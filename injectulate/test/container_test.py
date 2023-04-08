from injectulate import Container


def test_container_can_be_created():
    container = Container()
    assert container is not None
    assert isinstance(container, Container)


def test_multiple_containers_are_the_same_container():
    c1 = Container()
    c2 = Container()
    assert c1 == c2


class SimpleClass:
    pass


def test_container_can_create_test_class():
    target = Container()
    result = target.get(SimpleClass)
    assert isinstance(result, SimpleClass)


class ClassWithPrimitiveConstructorParameters:
    def __init__(self, an_int, a_str):
        assert isinstance(an_int, int)
        assert isinstance(a_str, str)
        self.an_int = an_int
        self.a_str = a_str


def test_can_create_class_and_pass_parameters():
    target = Container()
    result = target.get(ClassWithPrimitiveConstructorParameters, 2, "stuff")
    assert isinstance(result, ClassWithPrimitiveConstructorParameters)
    assert result.an_int == 2
    assert result.a_str == "stuff"
