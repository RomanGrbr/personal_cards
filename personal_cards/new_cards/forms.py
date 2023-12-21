from django import forms
from django.forms import ValidationError

from .models import Card, Attribute

FORM_TYPES = {
    'audio': forms.FileField,
    'boolean': forms.BooleanField,
    'text': forms.CharField,
    'choice': forms.ChoiceField,
    'date': forms.DateField,
    'datetime': forms.DateTimeField,
    'decimal': forms.DecimalField,
    'duration': forms.DurationField,
    'email': forms.EmailField,
    'file': forms.FileField,
    'float': forms.FloatField,
    'ipaddress': forms.GenericIPAddressField,
    'image': forms.ImageField,
    'integer': forms.IntegerField,
    'nullboolean': forms.NullBooleanField,
    'slug': forms.SlugField,
    'time': forms.TimeField,
    'url': forms.URLField,
    'uuid': forms.UUIDField,
    'video': forms.FileField,
}


class ImageAttributeForm(forms.Form):
    files = forms.ImageField(label='Изображение', required=False)
    files.widget.attrs['multiple'] = True


class FileAttributeForm(forms.Form):
    files = forms.FileField(label='Файл', required=False)
    files.widget.attrs['multiple'] = True


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = '__all__'


class DynamicFormCreator(forms.Form):

    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(DynamicFormCreator, self).__init__(*args, **kwargs)
        for n, field in enumerate(extra):
            try:
                self.fields[f'{n}_custom_{field.field_name}'] = FORM_TYPES[
                    str(field.attr_type)
                ](
                    label=field.label,
                    help_text=field.help_text,
                    required=False,
                    initial=getattr(field, 'value', None)
                )
            except KeyError:
                raise ValidationError(
                    '{} - {}'.format(
                        'Недопустимый тип поля', field.attr_type))
            except Exception as err:
                raise ValidationError(
                    '{} - {}'.format(
                        'Ошибка связанная с ', err))
            self.fields[f'{n}_custom_{field.field_name}'].widget.attrs['is_uniq'] = str(
                getattr(field, 'is_uniq')).lower
            self.fields[f'{n}_custom_{field.field_name}'].widget.attrs['attr_type'] = str(
                getattr(field, 'attr_type'))
            self.fields[f'{n}_custom_{field.field_name}'].widget.attrs['multiple'] = True
