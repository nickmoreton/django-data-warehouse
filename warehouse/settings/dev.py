from .base import *  # noqa

DEBUG = True


try:
    from .local_settings import *  # noqa
except ImportError:
    pass
