# encoding: utf-8

from django.db import models
from django.db.models.manager import BaseManager

from sphinxthat import fields, index, queryset


class SearchManager(BaseManager.from_queryset(queryset.SearchQuerySet)):
    pass


class SphinxIndex(index.SphinxIndexBase):
    class Meta:
        abstract = True
        model = None
