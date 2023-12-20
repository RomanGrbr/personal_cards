import base64
import uuid
import os

from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.forms.models import model_to_dict

from cards.models import Card, Attribute, CardAttribute
from .forms import CardForm, DynamicAttrForm, FORM_TYPES

FILE = 'file'
IMAGE = 'image'
VIDEO = 'video'
AUDIO = 'audio'
FILE_FIELDS = [FILE, IMAGE, VIDEO, AUDIO]
PER_PAGE = 3


# TODO Нужен универсальный метод сохранения не только изображений
def save_image(folder, file):
    """Сохраняет изображение и возвращает путь с именем в uuid"""
    image_bytes = file.read()
    b_64img = str(base64.b64encode(image_bytes))
    filename = '{}.{}'.format(
        str(uuid.uuid5(uuid.NAMESPACE_X500, b_64img)),
        file.name.rsplit('.')[-1]
    )
    fs = FileSystemStorage()
    path = fs.save(f'{folder}/{filename}', file)
    file_url = fs.url(f'{folder}/{path}')
    return file_url


def delete_file(path: str) -> None:
    try:
        os.remove(f'{settings.BASE_DIR}{path}')
    except Exception as e:
        print(e)


def index(request):
    template = 'new_cards/card_list.html'
    context = {}

    cards = Card.objects.all().order_by('name')
    if request.GET.get('q'):
        query = request.GET.get('q')
        cards = cards.filter(
            Q(name__icontains=query) | Q(last_name__icontains=query)
        )
    paginator = Paginator(cards, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj

    card_form = CardForm(request.POST or None, request.FILES or None)
    context['card_form'] = card_form

    attr_form = DynamicAttrForm(request.POST or None, request.FILES or None)
    context['attr_form'] = attr_form

    if request.method == 'POST':
        if card_form.is_valid() and attr_form.is_valid():
            # Если полученное поле есть в основной модели, то сохраняем
            card = Card()
            for field in card._meta.get_fields():
                if field.name in card_form.cleaned_data:
                    setattr(card, field.name,
                            card_form.cleaned_data.get(field.name)
                            )
            card.save()

            attrs_objects = Attribute.objects.prefetch_related('attr_type')
            # Если поле есть в атрибутах, то валидируем и сохраняем
            attrs = []
            for attr in attrs_objects:
                if attr.field_name in attr_form.data:
                    for value in dict(attr_form.data).get(attr.field_name):
                        if value and attr_form.fields.get(attr.field_name).clean(value):
                            # TODO Тут можно добавить дополнительную валидацию
                            attrs.append(
                                CardAttribute(
                                    id_attribute=attr,
                                    id_card=card,
                                    value=value
                                )
                            )

            # Если поле есть в атрибутах, то сохраняем файл в директорию
            # соответствующую типу атрибута, путь сохраняем в атрибут
            for attr in attrs_objects:
                if attr.field_name in dict(request.FILES):
                    values = dict(request.FILES).get(attr.field_name)
                    # TODO Тут можно добавить дополнительную валидацию
                    for value in values:
                        folder = save_image(attr.attr_type, value)
                        attrs.append(
                            CardAttribute(
                                id_attribute=attr,
                                id_card=card,
                                value=folder
                            )
                        )
            CardAttribute.objects.bulk_create(attrs)
    return render(request, template, context)


def card_info(request, card_id):
    """Детальная информация записи"""
    template = 'cards/card_info.html'
    context = {}
    card = get_object_or_404(Card, pk=card_id)
    # card_data = card.attrs.add_attrs_annotations().exclude(
    #     attr_type__in=FILE_FIELDS)
    card_form = CardForm(initial=model_to_dict(card))
    context['card_form'] = card_form
    # if request.method == 'POST':
    #     for file in card_data:
    #         del_file_from_folder(file.value)
    #     del_file_from_folder(f'{settings.MEDIA_URL}{card.avatar}')
    #     card.delete()
    #     return redirect('new_cards:list')
    return render(request, template, context)
