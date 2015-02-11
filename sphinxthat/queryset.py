# encoding: utf-8

from django.utils.six import wraps
from sphinxit.core.helpers import BaseSearchConfig
from sphinxit.core.processor import Search

from sphinxthat.index import SphinxModelRegister


class SphinxItConfig(BaseSearchConfig):
    WITH_STATUS = False
    DEBUG = False


class ExtendedSearch(Search):
    def clone(self):
        return self.filter()


class SearchQuerySet(object):
    """
    QuerySet-like object and proxy to `sphinxit.core.processorSearch`
    """

    def __init__(self, model=None, using=None, query=None, hints=None):
        self.index = SphinxModelRegister()[model]
        self.model = model
        query = query or ExtendedSearch(indexes=[self.index.index_name()],
                                        config=SphinxItConfig)
        self.query = query

    def count(self):
        data = self.query.limit(0, 1).ask()
        return int(data['result']['meta']['total'])

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self.clone(query=self.limit(item.start, item.stop - item.start))
        return iter(self)

    def __getattribute__(self, name):
        try:
            return super(SearchQuerySet, self).__getattribute__(name)
        except AttributeError:
            attr = getattr(self.query, name)
            if callable(attr):
                return self._wrap_search_method(attr)
            return attr

    def _wrap_search_method(self, method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            result = method(*args, **kwargs)
            if isinstance(result, ExtendedSearch):
                return self.clone(query=result)
            return result
        return wrapper

    def __len__(self):
        return self.count()

    def clone(self, **kwargs):
        kwargs.setdefault('model', self.model)
        kwargs.setdefault('query', self.query.clone())
        return self.__class__(**kwargs)

    def __iter__(self):
        items = self.select('id').ask()['result']['items']
        primary_keys = (item['id'] for item in items)

        qs = self.index.search_queryset(primary_keys)

        return iter(qs)

    def none(self):
        return []
