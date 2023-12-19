from itertools import chain

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView
from django.conf import settings
from django.core.paginator import Paginator

from .forms import CardForm, CardAttributeForm
from .models import Attribute, Card, CardAttribute
from .utils import get_data, image_save, del_file_from_folder


FILE_FIELDS = ['FileField', 'ImageField']
PER_PAGE = 3

def method_save_card_files(files: dict) -> list:
    """Сохранить файлы из files"""
    save_files = []
    for key, value in files.items():
        for n, file in enumerate(value):
            folder = image_save(file)
            save_files.append({f'{n}_{key}': folder})
    return save_files


def get_bulk_item(card: Card, key: str, value) -> CardAttribute:
    """Возвращает объект CardAttribute если есть Attribute"""
    name = key.split('_')[-1]
    attr = Attribute.objects.filter(field_name=name)
    if attr:
        return CardAttribute(
            id_attribute=attr.first(),
            id_card=card,
            value=value
        )


def method_save_card(card: Card, form: CardForm, files: dict = None) -> None:
    """Сохраняет полученные данные в форме в модель Card"""
    attrs = []
    # Если есть файлы, то сохранить их и добавить в cleaned_data
    if files:
        for file in method_save_card_files(files):
            form.cleaned_data.update(file)
    for key, value in form.cleaned_data.items():
        if value and not isinstance(value, InMemoryUploadedFile):
            attr = get_bulk_item(card=card, key=key, value=value)
            if attr:
                attrs.append(attr)
    new_args = get_data(dict(form.data))
    clean_data = form.my_validator_data(new_args)
    # Сохраняем записи без ошибок валидации
    for data in clean_data:
        if not data['error']:
            attrs.append(get_bulk_item(
                card=card, key=data['field_name'], value=data['value'])
            )
    CardAttribute.objects.bulk_create(attrs)


def save_new_data(card: Card, form, request) -> None:
    card.name = form.cleaned_data.pop('name')
    card.last_name = form.cleaned_data.pop('last_name')
    card.avatar = form.cleaned_data.pop('avatar')
    card.save()
    if request.FILES and request.FILES.get('avatar'):
        request.FILES.pop('avatar')
    method_save_card(
        card=card, form=form, files=dict(request.FILES) or None
    )


# def index(request):
#     """Получить все записи"""
#     template = 'cards/card_list.html'
#     context = {}
#     cards = Card.objects.all().order_by('name')
#     if request.GET.get('q'):
#         query = request.GET.get('q')
#         cards = cards.filter(
#             Q(name__icontains=query) | Q(last_name__icontains=query)
#         )
#     paginator = Paginator(cards, PER_PAGE)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context['page_obj'] = page_obj
#     return render(request, template, context)

def index(request):
    """Получить все записи и форму создания"""
    template = 'cards/card_list.html'
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

    extra = Attribute.objects.all()
    form = CardForm(request.POST or None, request.FILES or None, extra=extra)
    context['form'] = form
    # context['object_list'] = Card.objects.all()
    if request.method == 'POST':
        if form.is_valid():
            card = Card()
            save_new_data(card, form, request)
        return redirect('cards:card_info_or_delete', card_id=card.id)

    return render(request, template, context)


class CardListView(ListView):
    model = Card


def card_info_or_delete(request, card_id):
    """Детальная информация записи"""
    template = 'cards/card_info_or_delete.html'
    context = {}
    card = get_object_or_404(Card, pk=card_id)
    extra = card.attrs.add_attrs_annotations()
    form = CardForm(
        request.POST or None, initial=model_to_dict(card),
        extra=extra.exclude(attr_type__in=FILE_FIELDS)
    )
    context['form'] = form
    context['files'] = [
        file.value for file in extra.filter(attr_type__in=FILE_FIELDS)
    ]
    if request.method == 'POST':
        for file in extra.filter(attr_type__in=FILE_FIELDS):
            del_file_from_folder(file.value)
        del_file_from_folder(f'{settings.MEDIA_URL}{card.avatar}')
        card.delete()
        return redirect('cards:list')
    return render(request, template, context)


# TODO При изменении модели, добавить поля сохранения после валидности формы
def card_new(request):
    """Создать новую запись"""
    template = 'cards/card_new.html'
    context = {}
    extra = Attribute.objects.all()
    form = CardForm(request.POST or None, request.FILES or None, extra=extra)
    context['form'] = form
    context['object_list'] = Card.objects.all()
    if request.method == 'POST':
        if form.is_valid():
            card = Card()
            save_new_data(card, form, request)
        return redirect('cards:card_info_or_delete', card_id=card.id)
    return render(request, template, context)


def card_edit(request, card_id):
    """Редактировать запись"""
    template = 'cards/card_edit.html'
    context = {}
    card = get_object_or_404(Card, pk=card_id)
    extra = card.attrs.add_attrs_annotations()
    card_attrs_before = {attr.id: attr.field_name for attr in extra.exclude(
        attr_type__in=FILE_FIELDS)}
    clean_field_for_form = Attribute.objects.exclude(
        Q(field_name__in=card_attrs_before.values()) |
        Q(attr_type__attr_type__in=FILE_FIELDS)
    )
    form = CardForm(
        request.POST or None, request.FILES or None,
        initial=model_to_dict(card),
        extra=list(chain(
            clean_field_for_form,
            extra.exclude(attr_type__in=FILE_FIELDS)))
    )
    context['form'] = form
    if request.method == 'POST':
        if form.is_valid():
            # Удалить старые данные
            for attr in card.attrs.all():
                if attr.id_attribute.attr_type.attr_type in FILE_FIELDS:
                    continue
                else:
                    attr.delete()
            if card.avatar != form.cleaned_data.get("avatar"):
                del_file_from_folder(f'{settings.MEDIA_URL}{card.avatar}')
            save_new_data(card, form, request)
            context.update({'form': form})
            return redirect('cards:card_info_or_delete', card_id=card.id)
    return render(request, template, context)


def update_images(data):
    return [
        {'pk': data.id, 'image': data.value}
        for data in data
    ]


def card_gallery(request, card_id):
    template = 'cards/gallery.html'
    context = {}
    card = get_object_or_404(Card, pk=card_id)
    extra = card.attrs.add_attrs_annotations().filter(attr_type='ImageField')
    add_form = CardAttributeForm(request.POST or None, request.FILES or None)
    context['form'] = add_form
    context['card'] = card.id
    context['images'] = update_images(extra)
    if request.method == 'POST':
        if add_form.is_valid():
            image_type_attr = get_object_or_404(Attribute,
                attr_type__attr_type='ImageField')
            images = []
            for image in request.FILES.getlist('images'):
                images.append(CardAttribute(
                    id_attribute=image_type_attr,
                    id_card=card,
                    value=image_save(image)
                ))
            CardAttribute.objects.bulk_create(images)
        if 'del_image' in request.POST:
            attr_id = request.POST.get('del_image')
            attr = get_object_or_404(CardAttribute, pk=attr_id)
            del_file_from_folder(attr.value)
            attr.delete()
        extra = CardAttribute.objects.filter(
            id_card=card, id_attribute__attr_type__attr_type='ImageField')
        context.update({'images': update_images(extra)})
        return render(request, template, context)
    return render(request, template, context)
