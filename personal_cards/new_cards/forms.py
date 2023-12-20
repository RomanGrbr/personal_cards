from django import forms

from cards.models import Card, Attribute

FORM_TYPES = {
    'boolean': forms.BooleanField,
    'text': forms.CharField,
    'choice': forms.ChoiceField,
    'date': forms.DateField,
    'datetime': forms.DateTimeField,
    'decimal': forms.DecimalField,
    'duration': forms.DurationField,
    'email': forms.EmailField,
    'file': forms.FileField,
    'video': forms.FileField,
    'audio': forms.FileField,
    'float': forms.FloatField,
    'ipaddress': forms.GenericIPAddressField,
    'image': forms.ImageField,
    'integer': forms.IntegerField,
    'nullboolean': forms.NullBooleanField,
    'slug': forms.SlugField,
    'time': forms.TimeField,
    'url': forms.URLField,
    'uuid': forms.UUIDField,
}


class ItemsForm(forms.Form):
    pass


def dynamic_form_creator():
    """Создает форму с полями соответсвующих типов.
    На основе записей имен и типов полей в моедели Attribute

    """
    attr_fields = dict()
    for n, atr in enumerate(Attribute.objects.prefetch_related('attr_type')):
        if atr.attr_type.attr_type in FORM_TYPES:
            attr_fields[atr.field_name] = FORM_TYPES[atr.attr_type.attr_type](
                label=atr.label,
                help_text=atr.help_text,
                required=False,
                initial=getattr(atr, 'value', None)
            )
            attr_fields[atr.field_name].widget.attrs[
                'is_uniq'
            ] = 'true' if atr.is_uniq else None
    return type('DynamicItemsForm', (ItemsForm,), attr_fields)


DynamicAttrForm = dynamic_form_creator()


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = '__all__'
