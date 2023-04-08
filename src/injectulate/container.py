class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Container(metaclass=Singleton):
    def get(self, type_to_create, *args, **kwargs):
        return type_to_create(*args, **kwargs)
