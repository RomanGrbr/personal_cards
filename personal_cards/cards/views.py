import os
import uuid
import base64
from itertools import chain

from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.db.models import F, Q
from django.forms.models import model_to_dict

from .forms import ItemsForm, PersonForm, FORM_TYPES, CardForm, AgeForm
from .models import Attribute, Card, CardAttribute

from django import forms
from django.forms.models import inlineformset_factory, formset_factory


# attr_fields = {
#     atr.field_name: FORM_TYPES[atr.attr_type.attr_type](
#         label=atr.label,
#         help_text=atr.help_text,
#         # widget=forms.TextInput(
#         #     attrs={'is_uniq': atr.is_uniq}
#         # )
#     )
#     for atr in Attribute.objects.all()
# }

# attr_fields = dict()
# for atr in Attribute.objects.all():
#     attr_fields[atr.field_name] = FORM_TYPES[atr.attr_type.attr_type](
#         label=atr.label,
#         help_text=atr.help_text,
#         required=False,
#     )
#     attr_fields[atr.field_name].widget.attrs['is_uniq'] = atr.is_uniq
#
#
# DynamicItemsForm = type('DynamicItemsForm', (ItemsForm,), attr_fields)





def index(request):
    template = 'index.html'
    context = {
        'cards': Card.objects.all(),
    }
    return render(request, template, context)


def new_card(request, field_name=None):
    count_fields ={}
    for param, value in request.GET.items():
        if value.isdigit():
            count_fields[param] = int(value)
    template = 'new_card.html'
    context = {}
    person_form = PersonForm(request.POST or None, request.FILES or None)
    context['person_form'] = person_form
    context['forms'] = []
    for atr in Attribute.objects.all():
        attr_fields = dict()
        attr_fields[atr.field_name] = FORM_TYPES[atr.attr_type.attr_type](
            label=atr.label,
            help_text=atr.help_text,
            required=False
        )
        attr_fields[atr.field_name].widget.attrs['is_uniq'] = atr.is_uniq
        DynamicItemsForm = type('DynamicItemsForm', (ItemsForm,), attr_fields)
        if atr.field_name in count_fields:
            formset = formset_factory(DynamicItemsForm, extra=count_fields[atr.field_name])
        else:
            formset = formset_factory(DynamicItemsForm, extra=1)
        context['forms'].append(formset(request.POST or None, request.FILES or None, prefix=atr.field_name))
    if request.method == 'POST':
        if person_form.is_valid():
            print('person_form is valid')
        # for form in context['forms']:
            # for data in form.data:
            # print(form.data)
            # if form.is_valid():
                # print(form.cleaned_data)
                # print('form is valid')
    return render(request, template, context)

# def new_card(request):
#     template = 'card.html'
#     context = {}
#     # formset = formset_factory(FormAge, extra=2)
#     forms = []
#     # attr_fields = dict()
#     for atr in Attribute.objects.all():
#         attr_fields = dict()
#         attr_fields[atr.field_name] = FORM_TYPES[atr.attr_type.attr_type](
#             label=atr.label,
#             help_text=atr.help_text,
#             required=False
#         )
#         attr_fields[atr.field_name].widget.attrs['is_uniq'] = atr.is_uniq
#         DynamicItemsForm = type('DynamicItemsForm', (ItemsForm,), attr_fields)
#         forms.append(DynamicItemsForm)
#
#     form = forms
#     context['form'] = forms
#     if request.method == 'POST':
#         if form.is_valid():
#             print(form.data)
#         return render(request, template, context)
#     return render(request, template, context)

# Рабочий вариант
# def new_card(request):
#     template = 'card.html'
#     context = {}
#     # formset = formset_factory(FormAge, extra=2)
#     attr_fields = dict()
#     for atr in Attribute.objects.all():
#         attr_fields[atr.field_name] = FORM_TYPES[atr.attr_type.attr_type](
#             label=atr.label,
#             help_text=atr.help_text,
#             required=False
#         )
#         attr_fields[atr.field_name].widget.attrs['is_uniq'] = atr.is_uniq
#
#     DynamicItemsForm = type('DynamicItemsForm', (ItemsForm,), attr_fields)
#     form = DynamicItemsForm(request.POST or None)
#     context['form'] = form
#     if request.method == 'POST':
#         if form.is_valid():
#             print(form.data)
#         return render(request, template, context)
#     return render(request, template, context)


def image_save(file):
    tmp_file = ""
    if file:
        image_bytes = file.read()
        b_64img = str(base64.b64encode(image_bytes))
        filename = '{}.{}'.format(
            str(uuid.uuid5(uuid.NAMESPACE_X500, b_64img)),
            file.name.rsplit('.')[-1]
        )
        path = default_storage.save(filename,
                                    ContentFile(file.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
    return tmp_file


def card_save(form, card=Card()):
    for field in Card._meta.fields:
        if field.name in form.cleaned_data:
            field_value = form.cleaned_data.pop(field.name)
            setattr(card, field.name, field_value)
    card.save()
    return card


# def index(request):
#     template = 'index.html'
#     cards = Card.objects.all()
#     context = {
#         'cards': cards,
#     }
#     return render(request, template, context)


def card_edit(request, card_id=None):
    template = 'card.html'
    card = get_object_or_404(Card, pk=card_id)
    extra = card.attrs.select_related(
        'id_attribute', 'id_attribute__attr_type'
    ).annotate(
        field_name=F('id_attribute__field_name'),
        attr_type=F('id_attribute__attr_type__attr_type'),
        label=F('id_attribute__label'),
        help_text=F('id_attribute__help_text'),
        is_uniq=F('id_attribute__is_uniq')
    )
    # print('extra: {}'.format(extra))
    cadrd_arrts_before = {attr.id: attr.field_name for attr in extra}  # Атрибуты до редактирования
    # print('cadrd_arrts_before: {}'.format(cadrd_arrts_before))
    cadrd_arrts_after = set()
    form = CardForm(request.POST or None, request.FILES or None,
                    initial=model_to_dict(card), extra=list(chain(Attribute.objects.exclude(field_name__in=cadrd_arrts_before.values()), extra)))
    context = {
        'form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            card = card_save(form=form, card=card)
            # получил поле которое было добавлено
            for key, value in form.data.items():
                if key not in form.cleaned_data and key.startswith('custom'):
                    print('data_items -> key: {}, value: {}'.format(key, value))
            for key, value in form.cleaned_data.items():
                # print('form.cleaned_data -> key: {}, value: {}'.format(key, value))
                key_in_db = key.split('_')[-1]
                attr_id = int(form.fields[key].widget.attrs.get('id'))
                # Если есть значение и id цифра, если id был ранее и имя поля соответствует id
                if value:
                    if (attr_id in cadrd_arrts_before and
                            cadrd_arrts_before[attr_id] == key_in_db
                    ):
                        # print('Старый ключ: {}'.format(key))
                        # Тогда перезаписываем значения
                        if isinstance(value, InMemoryUploadedFile):
                            card_attr = get_object_or_404(CardAttribute,
                                                          pk=attr_id)
                            last_file_folder = card_attr.value
                            try:
                                os.remove(last_file_folder)
                            except Exception as e:
                                print(e)
                            finally:
                                file = form.cleaned_data.get(key)
                                value = image_save(file)
                        card_attr = get_object_or_404(CardAttribute, pk=attr_id)
                        card_attr.value = value
                        card_attr.save()
                        cadrd_arrts_after.add(attr_id)
                    else:
                        # print('Новый ключ: {}'.format(key))
                        attr = Attribute.objects.filter(field_name=key_in_db)
                        if attr:
                            if isinstance(value, InMemoryUploadedFile):
                                file = form.cleaned_data.get(key)
                                value = image_save(file)
                            CardAttribute.objects.create(
                                id_attribute=attr.first(),
                                id_card=card,
                                value=value
                            )
            print('cadrd_arrts_before -> {}'.format(cadrd_arrts_before))
            print('cadrd_arrts_after -> {}'.format(cadrd_arrts_after))
            for attr_id in (set(cadrd_arrts_before.keys()) - cadrd_arrts_after):
                card_attr = get_object_or_404(CardAttribute, pk=attr_id)
                card_attr.delete()
            context.update({'form': form})
            return render(request, template, context)
    return render(request, template, context)

# Рабочий вариант
# def new_card(request):
#     template = 'card.html'
#     extra = Attribute.objects.all()
#     form = CardForm(request.POST or None, request.FILES or None, extra=extra)
#     context = {
#         'form': form,
#     }
#     if request.method == 'POST':
#         if form.is_valid():
#             card = card_save(form=form)
#             for key, value in form.cleaned_data.items():
#                 key_in_db = key.split('_')[-1]
#                 if value:
#                     if isinstance(value, InMemoryUploadedFile):
#                         file = form.cleaned_data.get(key)
#                         value = image_save(file)
#                     attr = Attribute.objects.filter(field_name=key_in_db)
#                     if attr:
#                         CardAttribute.objects.create(
#                             id_attribute=attr.first(),
#                             id_card=card,
#                             value=value
#                         )
#         context.update({'form': form})
#         return render(request, template, context)
#     return render(request, template, context)


def card_delete(request, card_id):
    template = 'card.html'
    card = get_object_or_404(Card, pk=card_id)
    extra = CardAttribute.objects.filter(id_card=card_id).select_related(
        'id_attribute', 'id_attribute__attr_type'
    ).annotate(
        field_name=F('id_attribute__field_name'),
        attr_type=F('id_attribute__attr_type__attr_type'),
        label=F('id_attribute__label'),
        help_text=F('id_attribute__help_text'),
        is_uniq=F('id_attribute__is_uniq')
    )
    form = CardForm(request.POST or None, request.FILES or None,
                    initial=model_to_dict(card), extra=extra)
    context = {
        'form': form,
    }
    if request.method == 'POST':
        files = extra.filter(
            Q(attr_type='FileField') | Q(attr_type='ImageField')
        )
        for file in files:
            try:
                os.remove(file.value)
            except Exception as e:
                print(e)
        card.delete()
        return redirect('cards:index')
    return render(request, template, context)


def card_attr_delete(request, field_id):
    if request.method == 'POST':
        card_attr = get_object_or_404(CardAttribute, pk=field_id)
        print(card_attr)
    return redirect('cards:card_attr_delete')


