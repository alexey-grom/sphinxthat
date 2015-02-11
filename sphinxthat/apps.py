# encoding: utf-8

from django.apps import AppConfig

from sphinxthat.index import SphinxIndexRegister, SphinxModelRegister


def bind_managers():
    from sphinxthat.models import SearchManager

    for cls in SphinxIndexRegister().indexes():
        model = cls.meta.get_model()
        if model in SphinxModelRegister():
            continue

        SphinxModelRegister().add(model, cls)

        if not cls.meta.search_manager:
            continue
        SearchManager().contribute_to_class(model, cls.meta.search_manager)


class SphinxThatConfig(AppConfig):
    name = 'sphinxthat'

    def ready(self):
        super(SphinxThatConfig, self).ready()
        bind_managers()
