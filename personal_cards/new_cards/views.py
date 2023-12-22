import base64
import os
import uuid
from itertools import chain

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.db.models import FileField, ImageField, Q
from django.db.models.fields.files import FileField, ImageFieldFile
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .apps import NewCardsConfig
from .forms import FORM_TYPES, CardForm, DynamicFormCreator, ImageAttributeForm
from .models import Attribute, Card, CardAttribute

FILE = 'file'
IMAGE = 'image'
VIDEO = 'video'
AUDIO = 'audio'
FILE_FIELDS = [FILE, IMAGE, VIDEO, AUDIO]

CARD_LIST_TEMPLATE = f'{NewCardsConfig.name}/card_list.html'
CARD_LIST_URL = f'{NewCardsConfig.name}:card_list'
CARD_INFO_TEMPLATE = f'{NewCardsConfig.name}/card_info.html'
CARD_INFO_URL = f'{NewCardsConfig.name}:card_info'
CARD_EDIT_TEMPLATE = f'{NewCardsConfig.name}/card_edit.html'

PER_PAGE = 3


# TODO Нужен универсальный метод сохранения не только изображений
def save_image(folder: str, file) -> str:
    """Сохраняет изображение и возвращает путь с именем в uuid"""
    image_bytes = file.read()
    b_64img = str(base64.b64encode(image_bytes))
    filename = '{}.{}'.format(
        str(uuid.uuid5(uuid.NAMESPACE_X500, b_64img)),
        file.name.rsplit('.')[-1]
    )
    fs = FileSystemStorage()
    path = fs.save(f'{folder}/{filename}', file)
    return path


def delete_file(path: str) -> None:
    """Удалить файл из директории"""
    try:
        os.remove(f'{settings.BASE_DIR}/{settings.MEDIA_URL}/{path}')
    except Exception as e:
        print(e)


def extra_fields_data(data: dict) -> dict:
    """Из словаря с именами полей с custom в словарь с полями field_name"""
    clear_data = dict()
    for field, values in dict(data).items():
        for value in values:
            if value:
                name = field.split('_custom_')[-1]
                if name not in clear_data:
                    clear_data[name] = [value]
                else:
                    clear_data[name].append(value)
    return clear_data


def get_card_attr(attrs, card: Card, data: dict, file: bool = False) -> list:
    """Сбор полученных атрибутов и валидация, возвращает список объектов"""
    card_attrs = []
    attr_form_data = extra_fields_data(data)
    for attr in attrs:
        if attr.field_name in attr_form_data:
            for value in attr_form_data[attr.field_name]:
                # Создается поле формы соответствующего типа для фалидации
                field = FORM_TYPES[attr.attr_type.type_name]()
                clean_value = field.clean(value)
                # TODO Тут можно добавить дополнительную валидацию
                card_attrs.append(
                        CardAttribute(
                            attribute=attr,
                            card=card,
                            value=(save_image(attr.attr_type, clean_value)
                                   if file else clean_value)
                        )
                )
    return card_attrs


@require_http_methods(['GET', 'POST'])
def index(request):
    context = dict()

    cards = Card.objects.all()
    # TODO Заменить фильтрацию
    if request.GET.get('q'):
        query = request.GET.get('q')
        cards = cards.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
    paginator = Paginator(cards, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj

    card_form = CardForm(request.POST or None, request.FILES or None)
    context['form'] = card_form

    # DynamicAttrForm = dynamic_form_creator()
    attrs = Attribute.objects.all()
    attr_form = DynamicFormCreator(
        request.POST or None, request.FILES or None, extra=attrs)
    context['attr'] = attr_form
    if request.method == 'POST':
        if card_form.is_valid() and attr_form.is_valid():
            card = card_form.save()
            attrs_objects = Attribute.objects.prefetch_related('attr_type')
            attrs = []
            # Если поле есть в атрибутах, то валидируем и сохраняем
            attrs.extend(get_card_attr(
                attrs=attrs_objects, card=card, data=attr_form.data)
            )
            # Если поле есть в атрибутах, то сохраняем файл в директорию
            # соответствующую типу атрибута, путь сохраняем в атрибут
            attrs.extend(get_card_attr(
                attrs=attrs_objects, card=card, data=request.FILES, file=True)
            )
            CardAttribute.objects.bulk_create(attrs)
            return redirect(CARD_LIST_URL)
    return render(request, CARD_LIST_TEMPLATE, context)


@require_http_methods(['GET', 'POST'])
def card_info(request, card_id):
    """Детальная информация записи или удаление"""
    context = dict()
    card = get_object_or_404(Card, pk=card_id)
    context['form'] = CardForm(instance=card)

    attrs = card.card_attrs.add_attrs_annotations().exclude(
        attr_type__in=FILE_FIELDS)
    attr_form = DynamicFormCreator(
        request.POST or None, request.FILES or None, extra=attrs)
    context['attrs'] = attr_form
    if request.method == 'POST':
        for field, value in model_to_dict(card).items():
            if type(getattr(card, field)) in [ImageFieldFile, FileField]:
                delete_file(value)
        attr_files = card.card_attrs.add_attrs_annotations().filter(
            attr_type__in=FILE_FIELDS)
        for file in attr_files:
            delete_file(file.value)
        card.delete()
        return redirect(CARD_LIST_URL)
    return render(request, CARD_INFO_TEMPLATE, context)


@require_http_methods(['GET', 'POST'])
def card_edit(request, card_id):
    context = dict()

    card = get_object_or_404(Card, pk=card_id)
    card_form = CardForm(
        request.POST or None, request.FILES or None, instance=card)
    context['form'] = card_form

    extra = card.card_attrs.add_attrs_annotations().exclude(
                attr_type__in=FILE_FIELDS)
    card_attrs_before = [field.field_name for field in extra]
    clean_field_for_form = Attribute.objects.exclude(
        Q(field_name__in=card_attrs_before) |
        Q(attr_type__type_name__in=FILE_FIELDS)
    )
    attr_form = DynamicFormCreator(
        request.POST or None, request.FILES or None,
        extra=list(chain(
            clean_field_for_form,
            extra))
    )

    context['attr'] = attr_form
    if request.method == 'POST':
        if card_form.is_valid() and attr_form.is_valid():
            card = card_form.save()
            # Удалить все старые атрибуты кроме файлов
            for attr in card.card_attrs.add_attrs_annotations().exclude(
                attr_type__in=FILE_FIELDS):
                attr.delete()
            # Записать новые атрибуты
            attrs_objects = Attribute.objects.prefetch_related('attr_type')
            attrs = get_card_attr(
                attrs=attrs_objects, card=card, data=attr_form.data)
            CardAttribute.objects.bulk_create(attrs)
        return redirect(CARD_INFO_URL, card_id=card.id)
    return render(request, CARD_EDIT_TEMPLATE, context)


def update_files(data):
    """Обновить словарь изображений"""
    return [
        {'pk': data.id,
         'url': f'{settings.MEDIA_URL}/{data.value}'}
        for data in data
    ]


@require_http_methods(['GET', 'POST'])
def card_gallery(request, card_id):

    template = 'new_cards/gallery.html'
    context = {}
    card = get_object_or_404(Card, pk=card_id)
    extra = card.card_attrs.add_attrs_annotations().filter(attr_type=IMAGE)
    add_form = ImageAttributeForm(request.POST or None, request.FILES or None)
    context['form'] = add_form
    context['card'] = card
    context['files'] = update_files(extra)
    if request.method == 'POST':
        if add_form.is_valid():
            file_type_attr = get_object_or_404(
                Attribute, attr_type__type_name=IMAGE)
            files = []
            for file in request.FILES.getlist('files'):
                files.append(CardAttribute(
                    attribute=file_type_attr,
                    card=card,
                    value=save_image(file_type_attr.attr_type.type_name, file)
                ))
            CardAttribute.objects.bulk_create(files)
        if 'del_file' in request.POST:
            attr_id = request.POST.get('del_file')
            attr = get_object_or_404(CardAttribute, pk=attr_id)
            delete_file(attr.value)
            attr.delete()
        extra = CardAttribute.objects.filter(
            card=card, attribute__attr_type__type_name=IMAGE)
        context.update({'files': update_files(extra)})
        return render(request, template, context)
    return render(request, template, context)
