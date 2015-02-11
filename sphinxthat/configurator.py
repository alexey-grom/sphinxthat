# encoding: utf-8

from django.conf import settings
from django.utils import six, importlib

from sphinxthat import conf, templates
from sphinxthat.index import SphinxIndexRegister


class Configurator(object):
    def section_searchd(self):
        result = templates.SEARCH_TEMPLATE.format(pid_file=conf.pid_filename)
        return result.strip()

    def section_index(self, index):
        if index.meta.abstract:
            return ''

        qs = index.indexing_queryset()

        context = {}
        context.update({
            'database_{}'.format(key.lower()): value
            for key, value in six.iteritems(settings.DATABASES.get(qs.db))
        })
        context.update({
            'query': qs.query,
            'index_name': index.index_name(),
            'index_path': index.index_path(),
            'fields': '\n'.join([
                '{} = {}'.format(field.key, name)
                for name, field in six.iteritems(index.fields)
            ]),
            'source_type': index.source_type()
        })

        return templates.INDEX_TEMPLATE.format(**context).strip()

    def indexes(self):
        result = '\n'.join(self.section_index(item)
                           for item in SphinxIndexRegister().indexes())
        return result.strip()

    def general(self):
        result = templates.GENERAL_TEMPLATE.format(indexes=self.indexes(),
                                                   searchd=self.section_searchd())
        return result.strip()


def get_configurator():
    if not get_configurator._class:
        module, attr = conf.configurator_class.rsplit('.', 1)
        module = importlib.import_module(module)
        get_configurator._class = getattr(module, attr)()
    return get_configurator._class
get_configurator._class = None


def create_config_file():
    with file(conf.config_filename, 'w') as output:
        output.write(get_configurator().general())
