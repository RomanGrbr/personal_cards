from typing import List

from django import forms
from django.forms import ValidationError
from .models import CardAttribute

FORM_TYPES = {
    'BooleanField': forms.BooleanField,
    'CharField': forms.CharField,
    'ChoiceField': forms.ChoiceField,
    'DateField': forms.DateField,
    'DateTimeField': forms.DateTimeField,
    'DecimalField': forms.DecimalField,
    'DurationField': forms.DurationField,
    'EmailField': forms.EmailField,
    'FileField': forms.FileField,
    'VideoField': forms.FileField,
    'AudiField': forms.FileField,
    # 'FilePathField': forms.FilePathField(),
    'FloatField': forms.FloatField,
    'GenericIPAddressField': forms.GenericIPAddressField,
    'ImageField': forms.ImageField,
    'IntegerField': forms.IntegerField,
    'MultipleChoiceField': forms.MultipleChoiceField,
    'NullBooleanField': forms.NullBooleanField,
    # 'RegexField': forms.RegexField(),
    'SlugField': forms.SlugField,
    'TimeField': forms.TimeField,
    'TypedChoiceField': forms.TypedChoiceField,
    'TypedMultipleChoiceField': forms.TypedMultipleChoiceField,
    'URLField': forms.URLField,
    'UUIDField': forms.UUIDField,
}


class ImageAttributeForm(forms.Form):
    files = forms.ImageField(label='Изображение', required=False)
    files.widget.attrs['multiple'] = True


class FileAttributeForm(forms.Form):
    files = forms.FileField(label='Файл', required=False)
    files.widget.attrs['multiple'] = True


class ItemsForm(forms.Form):
    pass


# TODO Не используется, запасной вариант
def dynamic_form_creator(atrr_class):
    """Создает форму с полями соответсвующих типов.
    На основе записей имен и типов полей в моедели Attribute

    """
    attr_fields = dict()
    for n, atr in enumerate(atrr_class.objects.all()):
        attr_fields[atr.field_name] = FORM_TYPES[atr.attr_type.attr_type](
            label=atr.label,
            help_text=atr.help_text,
            required=False,
            initial=getattr(atr, 'value', None)
        )
        attr_fields[atr.field_name].widget.attrs['is_uniq'] = atr.is_uniq
    return type('DynamicItemsForm', (ItemsForm,), attr_fields)


class CardForm(forms.Form):
    name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    avatar = forms.ImageField(label='Аватарка')

    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(CardForm, self).__init__(*args, **kwargs)
        for n, field in enumerate(extra):
            try:
                self.fields[f'custom_{n}_{field.field_name}'] = FORM_TYPES[
                    getattr(field.attr_type, 'attr_type', field.attr_type)](
                    label=field.label,
                    help_text=field.help_text,
                    required=False,
                    initial=getattr(field, 'value', None)
                )
            except KeyError:
                raise ValidationError(
                    '{} - {}'.format(
                        'Недопустимый тип поля', field.attr_type.attr_type))
            except Exception as err:
                raise ValidationError(
                    '{} - {}'.format(
                        'Ошибка связанная с ', err))
            self.fields[f'custom_{n}_{field.field_name}'].widget.attrs['is_uniq'] = str(
                getattr(field, 'is_uniq')).lower
            self.fields[f'custom_{n}_{field.field_name}'].widget.attrs['attr_type'] = str(
                getattr(field, 'attr_type'))
        #     self.fields[f'custom_{n}_{field.field_name}'].widget.attrs[f'custom_id_{n}'] = str(
        #         getattr(field, 'id'))
            self.fields[f'custom_{n}_{field.field_name}'].widget.attrs['multiple'] = True

    def my_validator_data(self, new_arrg: list) -> List[dict]:
        """Валидация значений полей не попавших в cleaned_data.
        Сопоставляет имя нового поля с имеющимися в форме,
        если поле есть, то создает аналогичный тип поля и валидирует.

        """
        valid_data = []
        for item in new_arrg:
            for field_name, data in item.items():
                if field_name in self.fields:
                    new_field = self.fields[field_name].__class__()
                    error_message = None
                    try:
                        new_field.clean(data)
                    except ValidationError as err:
                        error_message = err
                    finally:
                        obj = {
                            'field_name': field_name,
                            'attr_type': self.fields[field_name].__class__,
                            'value': data,
                            'error': error_message
                        }
                        valid_data.append(obj)

        return valid_data