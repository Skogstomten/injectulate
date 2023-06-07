# Injectulate
Lightweight dependency injection framework relying on type annotations for dependency resolution.

## Installation
`pip install injectulate`

## Usage

### Simple use case
```python
from injectulate import Builder


class Foo:
    pass


builder = Builder()
container = builder.build()

foo = container.get(Foo)
```

### Simple dependencies
```python
from injectulate import Builder


class Foo:
    pass


class Bar:
    # Type annotation is required as it's used to resolve the dependency.
    def __init__(self, dependency: Foo):
        pass


container = Builder().build()

bar = container.get(Bar)
```
A class with a dependency on `Container` will always result in the container injecting itself.

### Binding class to inheriting class
```python
from injectulate import Builder
from abc import ABC


class AbstractClass(ABC):
    pass


class Implementation(AbstractClass):
    pass


builder = Builder()
builder.bind(AbstractClass).to(Implementation)
container = builder.build()

impl = container.get(AbstractClass)
```

### Binding to factory method
```python
from injectulate import Builder, Container
from abc import ABC


class AbstractClass(ABC):
    pass


class Implementation(AbstractClass):
    def __init__(self, c: Container):
        pass


builder = Builder()
builder.bind(AbstractClass).to(lambda c: Implementation(c))
container = builder.build()

impl = container.get(AbstractClass)
```

### Suggestions
Are welcomed