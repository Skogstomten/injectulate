from inspect import signature as get_signature, Signature, Parameter


class Container:
    def get(self, cls: type, *args, **kwargs):
        """

        :param cls:
        :param args:
        :param kwargs:
        :return:
        """
        if cls == Container:
            return self
        signature = get_signature(cls.__init__)
        arguments: list = self._resolve_dependencies(signature)
        return cls(*arguments, *args, **kwargs)

    def _resolve_dependencies(self, signature: Signature) -> list:
        """

        :param signature:
        :return:
        """
        arguments = []
        if len(signature.parameters) == 1:
            return arguments
        for parameter in signature.parameters.values():
            # noinspection PyUnusedLocal,PyShadowingNames
            match parameter:
                case Parameter(name="self") | Parameter(name="args") | Parameter(name="kwargs"):
                    continue
                case Parameter(annotation=Container):
                    arguments.append(self)
                case _:
                    dependency_signature = get_signature(parameter.annotation.__init__)
                    arguments + self._resolve_dependencies(dependency_signature)
        return arguments
