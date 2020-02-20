import inspect
import logging
import typing
from typing import Type, Dict, Union, Callable, Any, Optional, Hashable

from . import exceptions
from .injector import Injector

TProvider = Union[Type, Callable[[Type], Type]]
TContext = Optional[Dict[Type, TProvider]]


logger = logging.getLogger(__name__)


class Container(Injector):
    _VAR_KIND_PARAMETER = object()

    def __init__(
        self,
        context: TContext = None,
        parent: 'Container' = None,
    ):
        super().__init__()

        self._instances = dict()
        self.context = context or {}
        self._parent = parent

    def get(
        self,
        key: Hashable,
        context: TContext = None
    ):
        context = context or {}

        try:
            klass = self.get_injectable(key)
            return self._get(klass)
        except exceptions.NonInjectableClass:
            parent_context = {
                **self.context,
                **context
            }

            logging.debug(
                'getting key=%s, context=%s',
                key, parent_context
            )

            if self._parent:
                return self._parent.get(key, parent_context)
            raise

    def _get(self, key: Hashable):
        if not self.is_singleton(key):
            klass = self.get_injectable(key)
            return self._instantiate(klass)

        if key not in self._instances:
            klass = self.get_injectable(key)
            self._instances[key] = self._instantiate(klass)

        return self._instances[key]

    def _instantiate(self, key: Type) -> Any:
        if key in self.context:
            return self.context[key](self)

        if not self.is_injectable(key):
            raise exceptions.NonInjectableClass(
                f'{key} is non injectable', key
            )

        parameters = inspect.signature(key.__init__).parameters
        args = list(parameters.values())[1:]
        args = [
            self._get_argument(arg, key) for arg in args
        ]
        args = list(filter(
            lambda it: it is not self._VAR_KIND_PARAMETER, args
        ))

        instance = key(*args)

        logger.debug(
            'instantiate klass=%s, args=%s, instance=%s',
            key, args, instance
        )

        return instance

    def _get_argument(self, param: inspect.Parameter, key: Type):
        annotations = self.__extract_types(param)

        if param.kind in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        ):
            return self._VAR_KIND_PARAMETER

        for annotation in annotations:
            if annotation in self.context:
                logger.debug(
                    'use context=%s, key=%s, param=%s',
                    self.context,
                    key,
                    param,
                )
                if inspect.isfunction(self.context[annotation]):
                    return self.context[annotation](self)
                else:
                    return self.context[annotation]
            if self.is_injectable(annotation):
                return self.get(annotation)
            elif annotation is None.__class__:  # optional argument
                return None

        if self._parent:
            return self._parent._get_argument(param, key)

        raise exceptions.NonInjectableArgument(
            'Non injectable argument',
            key,
            param.name,
            param.annotation
        )

    def __extract_types(
        self, param: inspect.Parameter,
    ) -> typing.Tuple[Type, ...]:
        if hasattr(param.annotation, '__args__'):
            return param.annotation.__args__

        return param.annotation,


injectable = Container()
