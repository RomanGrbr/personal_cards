import os
from itertools import chain

from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from django.forms.models import model_to_dict

from .forms import CardForm
from .models import Attribute, Card, CardAttribute
from .utils import image_save, get_data, card_annotate


def method_save_card(card: Card, form: CardForm) -> None:
    for key, value in form.cleaned_data.items():
        if value:
            if isinstance(value, InMemoryUploadedFile):
                file = form.cleaned_data.get(key)
                value = image_save(file)
            name = key.split('_')[-1]
            attr = Attribute.objects.filter(field_name=name)
            if attr:
                CardAttribute.objects.create(
                    id_attribute=attr.first(),
                    id_card=card,
                    value=value
                )

    new_arrg = get_data(dict(form.data))
    clean_data = form.my_validator_data(new_arrg)
    for data in clean_data:
        if not data['error']:
            if isinstance(data['attr_type'], InMemoryUploadedFile):
                data['value'] = image_save(data['value'])
            name = data['field_name'].split('_')[-1]
            attr = Attribute.objects.filter(
                field_name=name
            )
            if attr:
                CardAttribute.objects.create(
                    id_attribute=attr.first(),
                    id_card=card,
                    value=data['value']
                )


def index(request):
    template = 'index.html'
    context = {
        'cards': Card.objects.all(),
    }
    return render(request, template, context)


def card_new(request):
    template = 'card.html'
    extra = Attribute.objects.all()
    form = CardForm(request.POST or None, request.FILES or None, extra=extra)
    context = {
        'form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            card = Card()
            card.name = form.cleaned_data['name']
            card.last_name = form.cleaned_data['last_name']
            card.save()
            method_save_card(card, form)
        return redirect('cards:card_edit', card_id=card.id)
    return render(request, template, context)


def card_edit(request, card_id):
    template = 'card.html'
    card = get_object_or_404(Card, pk=card_id)
    extra = card_annotate(card)
    cadrd_arrts_before = {attr.id: attr.field_name for attr in extra}
    form = CardForm(
        request.POST or None, request.FILES or None,
        initial=model_to_dict(card),
        extra=list(chain(
            Attribute.objects.exclude(
                field_name__in=cadrd_arrts_before.values()), extra)
        )
    )
    context = {
        'form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            card.name = form.cleaned_data['name']
            card.last_name = form.cleaned_data['last_name']
            # удалить старые данные
            for attr in card.attrs.all():
                if attr.id_attribute.attr_type.attr_type in ['FileField', 'ImageField']:
                    try:
                        os.remove(attr.value)
                    except Exception as e:
                        print(e)
                attr.delete()
            card.save()
            method_save_card(card, form)
            context.update({'form': form})
            return redirect('cards:card_edit', card_id=card.id)
    return render(request, template, context)


def card_delete(request, card_id):
    template = 'card.html'
    card = get_object_or_404(Card, pk=card_id)
    extra = card_annotate(card)
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
