# encoding: utf-8

from abc import abstractproperty, ABCMeta

from django.utils import six


class FieldType(six.with_metaclass(ABCMeta, object)):
    @abstractproperty
    def key(self):
        pass


class TextField(FieldType):
    key = 'sql_field_string'


class StringField(FieldType):
    key = 'sql_attr_string'


class IntField(FieldType):
    key = 'sql_attr_uint'


class BigIntField(FieldType):
    key = 'sql_attr_bigint'


class FloatField(FieldType):
    key = 'sql_attr_float'


class BoolField(FieldType):
    key = 'sql_attr_bool'


class TimestampField(FieldType):
    key = 'sql_attr_timestamp'
