# encoding: utf-8

import sys
from os.path import join

from django.conf import settings


config = {
    'configurator_class': 'sphinxthat.configurator.Configurator',
    'config_filename': join(settings.BASE_DIR, 'sphinx.conf'),
    'index_path': join(settings.BASE_DIR, '_index/'),
    'pid_filename': join(settings.BASE_DIR, 'searchd.pid'),
}
config.update(getattr(settings, 'SEARCH', {}))


class Wrapper(object):
    def __init__(self, wrapped):
        super(Wrapper, self).__init__()
        self.wrapped = wrapped

    def __getattribute__(self, name):
        try:
            return super(Wrapper, self).__getattribute__(name)
        except AttributeError:
            return self.wrapped.config[name]


sys.modules[__name__] = Wrapper(sys.modules[__name__])
