import os
from datetime import datetime, timedelta
import json
# from .decode import decodeBasicAuth

import requests
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from pkt_fpk.settings import (BASE_DIR, MAC_LABEL, MEDIA_ROOT, PAO_PASS,
                              PAO_URL, PAO_USER, MEDIA_URL, PAO_FACE_URL,
                              PAO_VOICE_URL)
from .actuvity_logger import ActivityLogMixin
from .constants import AUDIO, FILE, IMAGE, MOVE
from .elastic_serach import (get_search_index, get_search_scs_page,
                             get_search_scs_page_for_name, get_search_smi)
from .filters import AttributeFilter, CardAttributeFilter
from .get_bio_model import get_bio_model, read_file_and_base64
from .models import Attribute, Card, CardAttribute, SocialNetwork
from .serializers import (AttributeSerializer, CardAttributeSerializer,
                          CardSerializer, SocialNetworkSerializer)
from .utils import delete_file, get_image, save_file
# from django.db import reset_queries, connection

class CardViewSet(ActivityLogMixin, ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('full_name', 'attrs__value',)

    def get_card(self, pk: int) -> Card:
        """Получить карточку по pk"""
        return get_object_or_404(self.queryset, pk=pk)
    
    def perform_destroy(self, instance):
        """Удалить все файлы перед удалением объекта."""
        files = instance.attrs.filter(
            attribute__attr_type__type_name__in=[AUDIO, FILE, IMAGE, MOVE])
        for file in files:
            delete_file('{}/{}'.format(BASE_DIR, file.value))
        delete_file('{}/{}'.format(MEDIA_ROOT, instance.avatar))
        super().perform_destroy(instance)

    @staticmethod
    def get_network_confirmed(
            card: Card, source='', collapse=True, social_id=None) -> list:
        """Подтвержденные страницы соц сетей по карточке."""
        social_pages = list()
        pages = card.social_networks.filter(
            social_id=social_id) if social_id is not None else card.social_networks.all()
        for page in pages:
            result = get_search_scs_page(
                social_id=page.social_id, source=source, collapse=collapse)
            for item in result:
                social_pages.append(item.to_dict())
        return social_pages
    
    @staticmethod
    def get_social_network_found(card: Card, source: str) -> list:
        """Все найденные страницы соц сетей по карточке."""
        social_pages = list()
        result = get_search_scs_page_for_name(
            phrase=card.full_name, source=source)
        for item in result:
            if not card.social_networks.filter(
                    social_id=item.to_dict().get('page').get('socialId')).exists():
                social_pages.append(item.to_dict())
        return social_pages

    @action(detail=True, methods=['GET'])
    def photo_search(self, request, pk: int):
        """Поиск по фото."""
        maclabel, PAO_USER, PAO_PASS = auth(request)
        response = requests.get(
            url=PAO_FACE_URL, params={'card_id': pk}, auth=(PAO_USER, PAO_PASS))
        try:
            data = response.json()
        except:
            return JsonResponse({'error': "Ошибка поиска"}, status=400)
        return JsonResponse({'result': data})

    @action(detail=True, methods=['GET'])
    def dictor_search(self, request, pk: int):
        """Поиск по дикторам."""
        maclabel, PAO_USER, PAO_PASS = auth(request)
        response = requests.get(
            url=PAO_VOICE_URL, params={'card_id': pk}, auth=(PAO_USER, PAO_PASS))
        try:
            data = response.json()
        except:
            return JsonResponse({'error': "Ошибка поиска"}, status=400)
        return JsonResponse({'result': data})

    @action(detail=True, methods=['GET'])
    def smi_search(self, request, pk: int):
        """Поиск публикаций в сми."""
        maclabel, PAO_USER, PAO_PASS = auth(request)
        time_zone = request.GET.get('time_zone', '+03:00')
        date_till = request.GET.get(
            'date_till', round(datetime.now().timestamp()))
        date_from = request.GET.get(
            'date_from', round((datetime.now() - timedelta(weeks=1)).timestamp()))
        with_aggs = request.GET.get('with_aggs', 'false').lower() == 'true'
        search_words_list = self.get_card(pk=pk).full_name.split()
        search_words1 = " AND ".join(search_words_list[0:2])
        search_words2 = " AND ".join(search_words_list)
        if search_words1 != search_words2:
            search_words = "({}) OR ({})".format(search_words1, search_words2)
        else:
            search_words = search_words1
        data = {
            "search_words": search_words,
            "search_type": "site",
            "date_name": "sort_date",
            "till": date_till,
            "from": date_from,
            "multi_lang": True,
            "sortorder": "desc",
            "sortby": "sort_date",
            "limit": 25,
            "offset": 0,
            "time_zone": time_zone,
            "with_aggs": with_aggs
        }
        response = requests.post(
            url=PAO_URL, json=data, auth=(PAO_USER, PAO_PASS))
        if with_aggs:
            statistics = {
                'labels': [],
                'datasets': [
                    {
                        'label': 'Количество упоминаний в СМИ',
                        'data': [],
                        'fill': False,
                        'lineTension': 0.5
                    }
                ]
            }
            for day in response.json()['statistics']['day_hist']:
                statistics['labels'].append(
                    datetime.fromtimestamp(day['key']).strftime('%Y-%m-%d'))
                statistics['datasets'][0]['data'].append(day['doc_count'])
            return JsonResponse({'statistics': [statistics]})
        resp = response.json()
        resp["search_words"] = search_words
        return JsonResponse(resp)
    
    @action(detail=True, methods=['GET'])
    def scs_search(self, request, pk: int):
        """Поиск в социальных сетях."""

        maclabel, PAO_USER, PAO_PASS = auth(request)
        socials_ids = [request.GET.get('social_id')]
        card = self.get_card(pk=pk)
        social_networks = card.social_networks.all()
        with_aggs = request.GET.get('with_aggs', 'false').lower() == 'true'
        if socials_ids[0] is None:
            socials_ids = [social.social_id for social in social_networks]
        data = {
            "search_words": "",
            "search_type": "net",
            "date_name": "sort_date",
            "till": round(datetime.now().timestamp()),
            "from": 0,
            "multi_lang": True,
            "source_list": socials_ids,
            "source_name": "author.socialId",
            "sortorder": "desc",
            "sortby": "sort_date",
            "limit": 25,
            "offset": 0,
            "with_aggs": with_aggs
        }
        if card.auto_collect or not social_networks.exists():
            data['search_words'] = card.full_name
            data['source_name'] = 'author.fullName'
            data['source_list'] = []
        response = requests.post(
            url=PAO_URL, json=data, auth=(PAO_USER, PAO_PASS))

        if with_aggs:
            statistics = {
                'labels': [],
                'datasets': [
                    {
                        'label': 'Количество публикаций',
                        'data': [],
                        'fill': False,
                        'lineTension': 0.5
                    }
                ]
            }
            for day in response.json()['statistics']['day_hist']:
                statistics['labels'].append(
                    datetime.fromtimestamp(day['key']).strftime('%Y-%m-%d'))
                statistics['datasets'][0]['data'].append(day['doc_count'])
            return JsonResponse({'statistics': [statistics]})
        return JsonResponse(response.json())

    @action(detail=True, methods=['POST'])
    def social_network(self, request, pk: int) -> Response:
        """Добавить страницу соц сети в подтвержденные."""
        card = self.get_card(pk=pk)
        socials = request.data.get('socials')
        source = request.data.get('source')
        for social_id in socials:
            data = {'card': card.id, 'social_id': social_id}
            serializer = SocialNetworkSerializer(
                data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
        card.auto_collect = False
        card.save()
        return Response({'pages': self.get_social_network_found(card, source)})

    @social_network.mapping.delete
    def delete_social_network(self, request, pk: int) -> Response:
        """Удалить страницу социальной сети из подтвержденных."""
        card = self.get_card(pk=pk)
        socials = request.data.get('socials')
        source = request.data.get('source')
        for social_id in socials:
            get_object_or_404(SocialNetwork,
                              card=self.get_card(pk=pk), social_id=social_id
                              ).delete()
        if not card.social_networks.exists():
            card.auto_collect = True
            card.save()
        return Response({'pages': self.get_network_confirmed(card, source)})

    @action(detail=True, methods=['GET'])
    def social_network_found(self, request, pk: int) -> Response:
        """Все найденные страницы соц сетей по карточке."""
        card = self.get_card(pk=pk)
        source = request.GET.get('source')
        return Response({'pages': self.get_social_network_found(card, source)})

    @action(detail=True, methods=['GET'])
    def social_network_confirmed(self, request, pk: int) -> Response:
        """Подтвержденные страницы соц сетей по карточке."""
        card = self.get_card(pk=pk)
        source = request.GET.get('source')
        return Response({'pages': self.get_network_confirmed(card, source)})

    @action(detail=True, methods=['GET'])
    def smi_about_person(self, request, pk: int) -> Response:
        """Сми о персоне."""
        result = get_search_smi(self.get_card(pk=pk).full_name)
        smi_about_person = list()
        for item in result:
            smi_about_person.append(item.to_dict())
        return Response({'smi': smi_about_person})

    @action(detail=True, methods=['GET'])
    def statistics(self, request, pk) -> Response:
        """Статистика по страницам соц сетей."""
        card = self.get_card(pk=pk)
        social_id = request.GET.get('social_id', None)
        pages = []
        if card.auto_collect:
            result = get_search_scs_page_for_name(
                phrase=card.full_name, source=False)
            for item in result:
                pages.append(item.to_dict())
        else:
            pages = self.get_network_confirmed(
                    card, collapse=False, social_id=social_id)
        statistics = list()
        followers = 'followersCount'
        followings = 'followingCount'
        posts = 'postsCount'
        friends = 'friendsCount'
        tables = [
            {'text': 'Число подписок персоны', 'data': followers},
            {'text': 'Число подписчиков персоны', 'data': followings},
            {'text': 'Число публикаций персоны', 'data': posts},
            {'text': 'Число друзей персоны', 'data': friends},
        ]

        labels = list()
        datasets = dict()
        users = list()
        curent_count = dict()
        for page in pages:
            label = '{} - {}'.format(
                page.get('sourceName'), page['page'].get('username'))
            date = datetime.fromtimestamp(page['scrapeTime']).strftime('%Y-%m-%d')
            if date not in labels:
                labels.append(date)
            if label not in datasets:
                users.append(page['page'].get('username'))
                datasets[label] = {
                    followers: list(),
                    followings: list(),
                    posts: list(),
                    friends: list(),
                    'label': ''
                }
                curent_count[label] = {
                    followers: 0,
                    followings: 0,
                    posts: 0,
                    friends: 0
                }
            datasets[label]['label'] = label

            cur_val = page['page'].get(followers, curent_count[label][followers])
            if cur_val == 0:
                cur_val = curent_count[label][followers]
            datasets[label][followers].append(cur_val)
            curent_count[label][followers] = cur_val

            cur_val = page['page'].get(followings, 0)
            if cur_val == 0:
                cur_val = curent_count[label][followings]
            datasets[label][followings].append(cur_val)
            curent_count[label][followings] = cur_val

            cur_val = page['page'].get(posts, 0)
            if cur_val == 0:
                cur_val = curent_count[label][posts]
            datasets[label][posts].append(cur_val)
            curent_count[label][posts] = cur_val


            cur_val = page['page'].get(friends, 0)
            if cur_val == 0:
                cur_val = curent_count[label][friends]
            datasets[label][friends].append(cur_val)
            curent_count[label][friends] = cur_val

        # Структура датасета определена в библиотеке фронта
        for table in tables:
            obj = {
                'text': table['text'],
                'labels': labels,
                'datasets': [
                    {
                        'label': item['label'],
                        'data': item[table['data']],
                        'fill': False,
                        'lineTension': 0.5
                    } for item in datasets.values()]
            }
            statistics.append(obj)

        all_followers = 0
        all_followings = 0
        all_posts = 0
        all_friends = 0
        for user, value in datasets.items():
            all_followers += value.get(followers)[-1]
            all_followings += value.get(followings)[-1]
            all_posts += value.get(posts)[-1]
            all_friends += value.get(friends)[-1]
        all_stats = {
            'users': ', '.join(users),
            followers: all_followers,
            followings: all_followings,
            posts: all_posts,
            friends: all_friends
        }
        return Response({'statistics': statistics, 'all_stats': all_stats})


class CardAttributeViewSet(ActivityLogMixin, ModelViewSet):
    queryset = CardAttribute.objects.add_attrs_annotations()
    serializer_class = CardAttributeSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = CardAttributeFilter

    def perform_destroy(self, instance):
        """Удалить файл перед удалением объекта."""
        if instance.attr_type in [AUDIO, FILE, IMAGE, MOVE]:
            delete_file('{}/{}'.format(BASE_DIR, instance.value))
        super().perform_destroy(instance)

    def get_serializer(self, *args, **kwargs):
        """Если получен файл, то сохраняется в соответствующую директорию."""
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        value = self.request.data.get("value")
        attribute_id = self.request.data.get("attribute")
        attribute = Attribute.objects.filter(pk=attribute_id).first()

        if value and attribute:
            draft_request_data = self.request.data.copy()
            if attribute.attr_type.type_name == IMAGE:
                file = get_image(value)
                value = save_file(folder=IMAGE, file=file)
            if attribute.attr_type.type_name == MOVE:
                value = save_file(folder=MOVE, file=value)
            if attribute.attr_type.type_name == AUDIO:
                value = save_file(folder=AUDIO, file=value)
            if attribute.attr_type.type_name == FILE:
                value = save_file(
                    folder=FILE,
                    file=value,
                    filename=value.name)
            draft_request_data["value"] = value
            kwargs["data"] = draft_request_data
            return serializer_class(*args, **kwargs)
        return serializer_class(*args, **kwargs)
    
    @action(detail=True, methods=['GET'])
    def get_bio_model(self, request, pk: int) -> Response:
        """Получение вектора для файлов."""
        media_type = request.GET.get('type', None)
        if media_type not in (AUDIO, IMAGE):
            return Response(
                {'message': 'Для этого типа файлов не реализован способ подтверждения'})
        media_attr = get_object_or_404(
            CardAttribute, pk=pk,
            attribute__attr_type__type_name=media_type)
        if media_attr.confirmed:
            media_attr.confirmed = False
            media_attr.vector_base = ''
            media_attr.save()
            return Response({'message': 'Подтверждение снято'})

        if media_type in (IMAGE,):
            media_attr.confirmed = True
            media_attr.save()
            return Response({'message': "Подтверждено"})

        media_db_path = media_attr.value.replace(MEDIA_URL, "")
        filepath = os.path.join(MEDIA_ROOT, media_db_path)
        file = read_file_and_base64(filepath)
        b64data = get_bio_model(file)
        if b64data.get('error'):
            return Response({'message': b64data.get('error')})
        media_attr.vector_base = b64data.get('b64data')
        media_attr.confirmed = True
        media_attr.save()
        return Response({'message': "Подтверждено"})


class AttributeViewSet(ReadOnlyModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = AttributeFilter


@api_view(['GET'])
def wiki_search(request) -> Response:
    """Поиск по вики."""
    keyword = request.GET.get('keyword', None)
    if keyword:
        cards = get_search_index(keyword)
        cards = [
            {
                'value': str(card.title),
                'label': str(card.title)
            } for card in cards]
        return Response({'cards': cards})
    return Response({'cards': '', })


@api_view(['GET'])
def social_search(request) -> Response:
    """Все найденные страницы соц сетей."""
    social_id = request.GET.get('social_id')
    username = request.GET.get('username')
    full_name = request.GET.get('full_name')
    source = request.GET.get('source')
    result = get_search_scs_page(
        social_id=social_id, username=username,
        full_name=full_name, source=source)
    pages = []
    for hit in result:
        pages.append(hit.to_dict())
    return Response({'pages': pages})


@api_view(['GET', 'POST'])
def maclabel(request) -> JsonResponse:
    """Получение текущей мандатной метки"""
    rows = []
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT user")
    #     rows = cursor.fetchall()
    REMOTE_USER = request.META.get('REMOTE_USER')
    if REMOTE_USER is None:
        return JsonResponse({}, status=401)
    result = {'Mac-Label': MAC_LABEL.get(request.META.get('Mac-Label')),
            #   'user': rows[0][0],
              'KRB5CCNAME': os.environ.get('KRB5CCNAME'),
              'REMOTE_USER': request.META.get('HTTP_X_REMOTE_USER')
              }
    return JsonResponse(result)

def auth(request):
    """ Записать в словарь пользователя и пароль из мета-данных запроса.

    Args:
        request (str): запрос, приходящий из интерфейса.
        db_conn (dict): данные для подключения к БД. словарь вида:
            {"NAME": 'имя БД', 'USER': 'пользователь БД', 'PASSWORD': 'пароль',
             'HOST': 'ip-адрес БД', 'PORT': 'порт БД'}. Если = None, то
            подключение будет по данным из config.json. """
    PAO_USER = None
    PAO_PASS = None
    try:
        kerb_name = request.META.get("KRB5CCNAME")

        maclabel = request.META['Mac-Label']
        if kerb_name:
            os.environ["KRB5CCNAME"] = kerb_name
            PAO_USER, PAO_PASS =\
                request.META["REMOTE_USER"], None
        # else:
        #     PAO_USER, PAO_PASS = decodeBasicAuth(
        #         request.META['HTTP_AUTHORIZATION'])
        return maclabel, PAO_USER, PAO_PASS
    except Exception as e:
        print(e)
        return 0, PAO_USER, PAO_PASS
