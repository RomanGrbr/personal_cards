from django import forms

from .models import Card


class AttrValueForm(forms.Form):
    company = forms.CharField(label='Компания')


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = '__all__'

        # def __init__(self, *args, **kwargs):
        #     extra = kwargs.pop('extra')
        #     super(CardForm, self).__init__(*args, **kwargs)
        #     for field in extra:
        #         print('{} - {}'.format(field.field, field.label))
        #         try:
        #             self.fields[field.field] = FORM_TYPES[field.atr_type.atr_type]
        #
        #         except KeyError:
        #             raise ValidationError(
        #                 '{} - {}'.format(
        #                     'Недопустимый тип поля', field.atr_type.atr_type))
        #         except Exception as err:
        #             raise ValidationError(
        #                 '{} - {}'.format(
        #                     'Ошибка связанная с ', err))
        #         # setattr(self.fields[field.field], 'label', field.label)
        #         self.fields[field.field].label = field.label
        #         self.fields[field.field].widget.attrs['is_uniq'] = str(
        #             field.is_uniq).lower
        #         self.fields[field.field].widget.attrs['atr_type'] = str(
        #             field.atr_type)
        #         if field.help_text:
        #             setattr(
        #                 self.fields[field.field],
        #                 'help_text', field.help_text
        #             )
        #     print(self.fields)
