# encoding: utf-8

from os.path import join
from weakref import WeakKeyDictionary

from django.db.models.loading import get_model
from django.utils import six

from sphinxthat import conf
from sphinxthat import fields as search_fields


class Register(object):
    _instance = None
    _register_class = dict

    def __new__(cls, *more):
        if not cls._instance:
            cls._instance = super(Register, cls).__new__(cls, *more)
            cls._instance._register = cls._register_class()
        return cls._instance

    def add(self, key, value):
        assert issubclass(value, SphinxIndexBase)
        self._register[key] = value


class SphinxIndexRegister(Register):
    def indexes(self):
        return six.itervalues(self._register)


class SphinxModelRegister(Register):
    _register_class = WeakKeyDictionary

    def __getitem__(self, item):
        return self._register[item]

    def __contains__(self, key):
        return key in self._register


class Properties(object):
    def __init__(self):
        self.abstract = False
        self.model = None
        self.search_manager = 'search'

    def get_model(self):
        model = self.model
        if model and isinstance(model, six.string_types):
            return get_model(model)
        return model

    def contribute_to_class(self, Class):
        Class.meta = self


class SphinxIndexMeta(type):
    def __new__(S, name, bases, namespace):
        Meta = namespace.pop('Meta', None)

        fields = {}
        for key in namespace.keys():
            value = namespace[key]
            if not isinstance(value, search_fields.FieldType):
                continue
            fields[key] = value
            namespace.pop(key)

        Class = super(SphinxIndexMeta, S).__new__(S, name, bases, namespace)

        Class.fields = fields

        meta = Properties()
        if Meta:
            for key, value in six.iteritems(Meta.__dict__):
                if key.startswith('_'):
                    continue
                setattr(meta, key, value)

        meta.contribute_to_class(Class)

        if not Class.meta.abstract:
            if not Class.meta.model:
                raise TypeError('Model required for "{}"!'.format(Class.__name__))
            SphinxIndexRegister().add(Class.__name__, Class)

        return Class


class SphinxIndexBase(six.with_metaclass(SphinxIndexMeta, object)):
    fields = None
    meta = None

    @classmethod
    def indexing_queryset(cls):
        return cls.meta.get_model().\
            objects.\
            values_list('id', *cls.fields.keys())

    @classmethod
    def search_queryset(cls, primary_keys):
        return cls.meta.get_model().\
            objects.\
            filter(pk__in=primary_keys)

    @classmethod
    def index_name(cls):
        return cls.meta.get_model()._meta.db_table

    @classmethod
    def index_path(cls):
        return join(conf.index_path, cls.index_name())

    @classmethod
    def source_type(cls):
        return 'mysql'

    class Meta:
        abstract = True
        model = None
