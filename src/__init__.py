from .container import Container, injectable

import logging

# TODO (VM): Get rid of this config
logging.basicConfig(
    level=logging.DEBUG,
    format='%(relativeCreated)6d %(threadName)s %(message)s'
)

__all__ = [
    'injectable', 'Container',
]
