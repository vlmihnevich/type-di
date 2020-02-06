from typing import Type


class InjectionError(Exception):
    pass


class NonInjectableClass(InjectionError):
    def __init__(
        self,
        msg: str,
        klass: Type,
    ):
        super().__init__(msg)
        self.klass = klass


class NonInjectableArgument(InjectionError):
    def __init__(
        self,
        msg: str,
        client: Type,
        argument_name: str,
        argument_type: Type
    ):
        super().__init__(msg)
        self.client = client
        self.argument_name = argument_name
        self.argument_type = argument_type
