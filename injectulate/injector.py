from typing import Type

from .container import Container


def inject(type_to_inject: Type):
    container = Container()
    return container.get(type_to_inject)
