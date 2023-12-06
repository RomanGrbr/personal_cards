import os
import uuid
import base64

from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django import forms
from django.db.models import F
from django.forms.models import model_to_dict

from .forms import CardForm
from .models import Attribute, Card, CardAttribute


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


def index(request):
    template = 'index.html'
    cards = Card.objects.all()
    context = {
        'cards': cards,
    }
    return render(request, template, context)


def card_edit(request, card_id=None):
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
        if form.is_valid():
            for field in Card._meta.fields:
                if field.name in form.cleaned_data:
                    field_value = form.cleaned_data.pop(field.name)
                    setattr(card, field.name, field_value)
            card.save()
            card = card_save(form=form, card=card)
            for key, value in form.cleaned_data.items():
                if value:
                    if isinstance(value, InMemoryUploadedFile):
                        file = form.cleaned_data.get(key)
                        value = image_save(file)
                    card_attribute = card.attrs.select_related(
                        'id_attribute'
                    ).get(id_attribute__field_name=key)
                    card_attribute.value = value
                    card_attribute.save()
            context.update({'form': form})
            return render(request, template, context)
    return render(request, template, context)


def new_card(request):
    template = 'card.html'
    extra = Attribute.objects.all()
    form = CardForm(request.POST or None, request.FILES or None, extra=extra)
    context = {
        'form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            card = card_save(form=form)
            for key, value in form.cleaned_data.items():
                if value:
                    if isinstance(value, InMemoryUploadedFile):
                        file = form.cleaned_data.get(key)
                        value = image_save(file)
                    attr = Attribute.objects.filter(field_name=key)
                    if attr:
                        CardAttribute.objects.create(
                            id_attribute=attr.first(),
                            id_card=card,
                            value=value
                        )
        context.update({'form': form})
        return render(request, template, context)
    return render(request, template, context)


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
        card.delete()
        return redirect('cards:index')
    return render(request, template, context)
