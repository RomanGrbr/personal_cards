import os
from itertools import chain

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CardForm
from .models import Attribute, Card, CardAttribute
from .utils import card_annotate, get_data, image_save, del_file_from_folder


def method_save_card_files(files: dict) -> list:
    """Сохранить файлы кроме последнего, он попадет в cleaned_data"""
    save_files = []
    for key, value in files.items():
        for n, file in enumerate(value[:len(value) - 1]):
            if isinstance(file, InMemoryUploadedFile):
                folder = image_save(file)
                save_files.append({
                    f'{n}_{key}': folder,
                })
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
        if value:
            # print(type(value))
            if isinstance(value, InMemoryUploadedFile):
                file = form.cleaned_data.get(key)
                value = image_save(file)
            attr = get_bulk_item(card=card, key=key, value=value)
            if attr:
                attrs.append(attr)
    new_args = get_data(dict(form.data))
    clean_data = form.my_validator_data(new_args)
    for data in clean_data:
        if not data['error']:
            attrs.append(get_bulk_item(
                card=card, key=data['field_name'], value=data['value'])
            )
    CardAttribute.objects.bulk_create(attrs)


def index(request):
    """Получить все записи"""
    template = 'index.html'
    context = {
        'cards': Card.objects.all(),
    }
    return render(request, template, context)


def card_new(request):
    """Создать новую запись"""
    template = 'card.html'
    extra = Attribute.objects.all()
    form = CardForm(request.POST or None, request.FILES or None, extra=extra)
    context = {
        'form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            card = Card()
            card.name = form.cleaned_data.pop('name')
            card.last_name = form.cleaned_data.pop('last_name')
            card.save()
            method_save_card(
                card=card, form=form, files=dict(request.FILES) or None)
        return redirect('cards:card_edit', card_id=card.id)
    return render(request, template, context)


def card_edit(request, card_id):
    """Редактировать запись"""
    template = 'card.html'
    card = get_object_or_404(Card, pk=card_id)
    extra = card_annotate(card)
    card_attrs_before = {attr.id: attr.field_name for attr in extra}
    form = CardForm(
        request.POST or None, request.FILES or None,
        initial=model_to_dict(card),
        extra=list(chain(
            Attribute.objects.exclude(
                field_name__in=card_attrs_before.values()), extra)
        )
    )
    context = {
        'form': form,
    }
    files_urls = [file.value for file in
                  extra.filter(attr_type__in=['FileField', 'ImageField'])
                  ]
    context.update({'files': files_urls})
    if request.method == 'POST':
        if form.is_valid():
            card.name = form.cleaned_data.pop('name')
            card.last_name = form.cleaned_data.pop('last_name')
            # удалить старые данные
            for attr in card.attrs.all():
                if attr.id_attribute.attr_type.attr_type in [
                    'FileField', 'ImageField'
                ]:
                    del_file_from_folder(attr.value)
                attr.delete()
            card.save()
            method_save_card(
                card=card, form=form, files=dict(request.FILES) or None
            )
            context.update({'form': form})
            return redirect('cards:card_edit', card_id=card.id)
    return render(request, template, context)


def card_delete(request, card_id):
    """Удалить запись"""
    template = 'card.html'
    card = get_object_or_404(Card, pk=card_id)
    extra = card_annotate(card)
    form = CardForm(request.POST or None, request.FILES or None,
                    initial=model_to_dict(card), extra=extra)
    context = {
        'form': form,
    }
    files_urls = [file.value for file in
                  extra.filter(attr_type__in=['FileField', 'ImageField'])
                  ]
    context.update({'files': files_urls})
    if request.method == 'POST':
        files = extra.filter(
            Q(attr_type='FileField') | Q(attr_type='ImageField')
        )
        for file in files:
            del_file_from_folder(file.value)
            # try:
            #     os.remove(file.value)
            # except Exception as e:
            #     print(f'При удалении {e}')
        card.delete()
        return redirect('cards:index')
    return render(request, template, context)
