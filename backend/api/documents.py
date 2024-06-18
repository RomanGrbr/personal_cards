from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from .models import MmdJSON, MmdMedia, PerObj, Post, ScsPage, SmiNews


@registry.register_document
class MmdMediaDocument(Document):

    class Index:
        name = 'mmd_media'

    class Django:
        model = MmdMedia


@registry.register_document
class MmdJSONDocument(Document):

    class Index:
        name = 'mmd_json'

    class Django:
        model = MmdJSON


@registry.register_document
class PerObjDocument(Document):

    class Index:
        name = 'per_obj'

    class Django:
        model = PerObj


@registry.register_document
class PostDocument(Document):

    class Index:
        name = 'scs_post'

    class Django:
        model = Post


@registry.register_document
class ScsPageDocument(Document):

    class Index:
        name = 'scs_page_*'

    class Django:
        model = ScsPage


@registry.register_document
class SmiNewsDocument(Document):

    class Index:
        name = 'smi_news_*_*'

    class Django:
        model = SmiNews
