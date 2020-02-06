from .container import Container, injectable
from .exceptions import InjectionError, NonInjectableArgument

import logging

# TODO (VM): Get rid of this config
logging.basicConfig(
    level=logging.DEBUG,
    format='%(relativeCreated)6d %(threadName)s %(message)s'
)

__all__ = [
    'injectable', 'Container'
]
