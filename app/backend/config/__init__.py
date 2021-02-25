import os

env = os.environ.get('ENVIRONMENT')


class ConfigurationNotFound(Exception):
    pass


if env == 'ENV':
    from .settings_env import *
else:
    raise ConfigurationNotFound()