import base64
import uuid
import os
from typing import List

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
from django.db.models import F


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


def get_data(form_data: dict) -> List[dict]:
    """Формирует список имен полей и значений не попавших в cleaned_data.
    Если длина полученного значения в data больше 1, то поле имеет
    дополнительные поля.
    Берется каждое значение до предпоследнего элемента и его имя поля,
    формируется список со словарями.

    """
    new_arrg_data = []
    for key, value in form_data.items():
        if len(value) > 1:
            for data in value[:len(value) - 1]:
                obj = {key: data}
                new_arrg_data.append(obj)
    return new_arrg_data


def card_annotate(card):
    """Аннотация модели Card атрибутами из связаннях таблиц"""
    return card.attrs.select_related(
                    'id_attribute', 'id_attribute__attr_type'
                ).annotate(
                    field_name=F('id_attribute__field_name'),
                    attr_type=F('id_attribute__attr_type__attr_type'),
                    label=F('id_attribute__label'),
                    help_text=F('id_attribute__help_text'),
                    is_uniq=F('id_attribute__is_uniq')
                )


# def validator_data(new_arrg: list, form) -> List[dict]:
#     """Валидация значений полей не попавших в cleaned_data.
#     Сопоставляет имя нового поля с имеющимися в форме,
#     если поле есть, то создает аналогичный тип поля и валидирует.
#
#     """
#     valid_data = []
#     for item in new_arrg:
#         for field_name, data in item.items():
#             if field_name in form.fields:
#                 new_field = form.fields[field_name].__class__()
#                 error_message = None
#                 try:
#                     new_field.clean(data)
#                 except ValidationError as err:
#                     error_message = err
#                 finally:
#                     obj = {
#                         'field_name': field_name,
#                         'attr_type': form.fields[field_name].__class__,
#                         'value': data,
#                         'error': error_message
#                     }
#                     valid_data.append(obj)
#
#     return valid_data


# TODO Работает но при сохранении и рендеренге теряются
#  дополнительные поля в инитерфейсе
# def new_card(request):
#     template = 'card.html'
#     context = {}
#     # Динамическое создание полей дополнительных атрибутов
#     DinamicForm = dynamic_form_creator(Attribute)
#     card_form = CardForm(request.POST or None, request.FILES or None)
#     dynamic_form = DinamicForm(request.POST or None, request.FILES or None)
#     context['card_form'] = card_form
#     context['dynamic_form'] = dynamic_form
#     if request.method == 'POST':
#         if card_form.is_valid() and dynamic_form.is_valid():
#             card = Card()
#             card.name = card_form.cleaned_data['name']
#             card.last_name = card_form.cleaned_data['last_name']
#             card.save()
#             for key, value in dynamic_form.cleaned_data.items():
#                 if value:
#                     if isinstance(value, InMemoryUploadedFile):
#                         file = dynamic_form.cleaned_data.get(key)
#                         value = image_save(file)
#                     name = key.split('_')[-1]
#                     attr = Attribute.objects.filter(field_name=name)
#                     if attr:
#                         CardAttribute.objects.create(
#                             id_attribute=attr.first(),
#                             id_card=card,
#                             value=value
#                         )
#             # Спиок имен полей и значений не попавших в cleaned_data
#             new_arrg = get_data(dict(dynamic_form.data))
#             # Валидация значений полей не попавших в cleaned_data
#             clean_data = validator_data(new_arrg, dynamic_form)
#             for data in clean_data:
#                 if not data['error']:
#                     if isinstance(data['attr_type'], InMemoryUploadedFile):
#                         file = dynamic_form.cleaned_data.get(data['value'])
#                         data['value'] = image_save(file)
#                     name = data['field_name'].split('_')[-1]
#                     attr = Attribute.objects.filter(
#                         field_name=name
#                     )
#                     CardAttribute.objects.create(
#                         id_attribute=attr.first(),
#                         id_card=card,
#                         value=data['value']
#                     )
#         context.update({'card_form': card_form})
#         context.update({'dynamic_form': dynamic_form})
#         return render(request, template, context)
#     return render(request, template, context)
