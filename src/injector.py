import logging
from typing import Type, Optional, Dict, Hashable

from . import exceptions


class Injector:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._injectable: Dict[Hashable, Type] = {}
        self._singletons: Dict[Hashable, Type] = {}

    def __call__(
        self,
        key: Optional[Hashable] = None,
        singleton: bool = True,
    ) -> Type:
        def wrapper(
            klass: Type,
        ):
            return self.register(key, klass, singleton)

        return wrapper

    def register(
        self,
        key: Hashable,
        klass: Type,
        singleton: bool
    ) -> Type:
        self._logger.debug(
            'register new class=%s, signleton=%s',
            klass, singleton
        )

        for inject_key in (key, klass):
            if not inject_key:
                continue

            self._injectable[inject_key] = klass
            if singleton:
                self._singletons[inject_key] = klass

        return klass

    def is_injectable(
        self,
        key: Hashable
    ) -> bool:
        return key in self._injectable

    def is_singleton(
        self, key: Type
    ) -> bool:
        return key in self._singletons

    def get_injectable(
        self, key: Type
    ) -> Type:
        if key not in self._injectable:
            raise exceptions.NonInjectableClass(
                f'{key} is non injectable or missing',
                key
            )
        return self._injectable[key]

    def reset(self):
        self._injectable = {}
        self._singletons = {}

