# encoding: utf-8

from sphinxthat import fields, index


class SphinxIndex(index.SphinxIndexBase):
    class Meta:
        abstract = True
        model = None
