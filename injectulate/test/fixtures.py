from pytest import fixture

from .. import Container


@fixture(autouse=True)
def clear_bindings():
    yield
    Container().clear()
