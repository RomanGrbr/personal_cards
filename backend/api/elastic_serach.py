from elasticsearch_dsl.query import SF, MultiMatch, Q

from .documents import (PerObjDocument, PostDocument, ScsPageDocument,
                        SmiNewsDocument)


def get_search_smi(phrase):
    """Поиск в СМИ о персоне."""
    query = Q('function_score', query=MultiMatch(
        fields=['org_keywords', 'title', 'cnt', 'person_keywords'],
        query=phrase))
    return SmiNewsDocument.search().query(query).extra(size=20).sort('-sort_date')


def get_search_index(phrase):
    """Поиск персональных карточек"""
    query = Q('function_score', query=MultiMatch(
        fields=['search_phr'], type='bool_prefix',
        query=phrase), functions=[SF('field_value_factor', field='weight')])
    return PerObjDocument.search().query(query)

# def get_search_posts(social_id):
#     """Поиск постов в социальных сетях"""
#     return PostDocument.search().query(
#         Q('match', author__socialId=social_id)
#         ).sort('-sort_date').extra(size=20).update_from_dict(
#             {'collapse': {'field': 'post.socialId'}}
#             )


def get_search_scs_page_for_name(phrase, source):
    """Поиск страниц в социальных сетях по fullName и username по заданной сети"""
    query = Q('match', page__fullName=phrase) | Q('match', page__username=phrase)
    if source:
        query = query & Q('match', sourceName=source)
    return ScsPageDocument.search().query(query).update_from_dict(
            {'collapse': {'field': 'page.socialId'}}
            ).sort('scrapeTime'
            ).extra(size=20)


def get_search_scs_page(
        username=None, social_id=None,
        full_name=None, source=None, collapse=True):
    """Поиск страниц в социальных сетях по socialId и заданной сети"""
    query = Q
    if social_id:
        query = Q('match', page__socialId=social_id)
    if username:
        query = Q('match', page__username=username)
    if full_name:
        query = Q('match', page__fullName=full_name)
    if source:
        query = query & Q('match', sourceName=source)
    if collapse:
        return ScsPageDocument.search().query(query).update_from_dict(
            {'collapse': {'field': 'page.socialId'}}
            ).sort('scrapeTime'
            ).extra(size=20)
    return ScsPageDocument.search().query(query).sort('scrapeTime'
            ).extra(size=10000)
