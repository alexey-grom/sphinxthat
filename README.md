sphinxthat
==========

Логическое дополнение [sphinxit](https://github.com/semirook/sphinxit) для интеграции в django-проект и решения вопросов напрямую несвязанных с SphinxQL.

Возможности:

- генерация конфига для sphinx на основе моделей
- управление демоном sphinx


Пример использования
====================

- регистрация моделей (в конфиге будет создан источник и индекс для sphinx)


    from sphinxthat.models import SphinxIndex, fields

    class Category(MPTTModel):
        # "ID категории";"Название категории";"Файл с раздачами"
    
        parent = TreeForeignKey('self', db_index=True, null=True, blank=True, related_name='children')
    
        active = models.BooleanField(default=True, db_index=True)
        name = models.CharField(max_length=128)
        slug = models.CharField(max_length=128, unique=True, db_index=True)
    
        count = models.IntegerField(default=0)
    
    class Torrent(models.Model):
        category = models.ForeignKey(Category, db_index=True, null=True, related_name='torrents')
    
        title = models.TextField()
    
        info_hash = models.CharField(max_length=255)
        size = models.BigIntegerField(null=True)
        registered = models.DateTimeField(null=True)
    
    class TorrentIndex(SphinxIndex):
        category_id = fields.IntField()
        title = fields.TextField()
        info_hash = fields.StringField()
        size = fields.BigIntField()
        registered = fields.TimestampField()
    
        class Meta:
            model = 'tracker.Torrent'
    
    class CategoryIndex(SphinxIndex):
        name = fields.TextField()
    
        class Meta:
            model = Category


- управление демоном (будет автоматически сгенерирован конфиг)


    $ ./manage.py sphinx_reindex
    $ ./manage.py sphinx_start
    
    
    
- поиск по индексам ([уже на основе возможностей sphinxit](http://sphinxit.readthedocs.org/en/latest/usage.html))


    from sphinxit.core.helpers import BaseSearchConfig
    from sphinxit.core.processor import Search
    
    from models import TorrentIndex
    
    class SphinxitConfig(BaseSearchConfig):
        WITH_STATUS = False
    
    search_query = Search(indexes=[TorrentIndex.index_name()], config=SphinxitConfig)
    search_query = search_query.match('nature')
    search_query = search_query.limit(0, 1000)

    
    