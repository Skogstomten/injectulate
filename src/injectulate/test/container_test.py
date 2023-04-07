from ..container import Container


def test_container_can_be_created():
    container = Container.get()
    assert container is not None
    assert isinstance(container, Container)


def test_multiple_containers_are_the_same_container():
    c1 = Container.get()
    c2 = Container.get()
    assert c1 == c2


def test_multiple_containers_are_the_same_container_with_init():
    c1 = Container()
    c2 = Container()
    assert c1 == c2
