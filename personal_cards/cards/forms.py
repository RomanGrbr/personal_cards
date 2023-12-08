from django import forms
from django.forms import ValidationError
from django.forms import ClearableFileInput, FileField
from django.core.validators import validate_image_file_extension

from .models import Card, CardAttribute


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


class CardForm(forms.Form):
    name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')

    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(CardForm, self).__init__(*args, **kwargs)
        for field in extra:
            try:
                self.fields[field.field_name] = FORM_TYPES[
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
            self.fields[field.field_name].widget.attrs['is_uniq'] = str(
                getattr(field, 'is_uniq')).lower
            self.fields[field.field_name].widget.attrs['attr_type'] = str(
                getattr(field, 'attr_type'))
            self.fields[field.field_name].widget.attrs['id'] = str(
                getattr(field, 'id'))
            # self.fields[field.field_name].widget.attrs['multiple'] = True

    def extra_fields(self):
        for name, value in self.cleaned_data.items():
            yield self.fields[name].label, value
