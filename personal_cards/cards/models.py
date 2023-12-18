from django.db import models
from django.db.models import F
MAX_LENGTH = 100


class AttributeType(models.Model):
    attr_type = models.CharField(
        'Тип атрибута (forms.fields)', max_length=MAX_LENGTH
    )

    class Meta:
        verbose_name = 'тип атрибута'
        verbose_name_plural = 'Типы атрибутов'

    def __str__(self):
        return self.attr_type


class Attribute(models.Model):
    field_name = models.CharField(
        'Имя поля', max_length=MAX_LENGTH, unique=True)
    attr_type = models.ForeignKey(
        AttributeType, on_delete=models.PROTECT, related_name='attributes',
        verbose_name='Тип атрибута (поля)'
    )
    label = models.CharField(
        'Название поля (label)', max_length=MAX_LENGTH)
    help_text = models.CharField(
        'Текст подсказка (help_text)', max_length=MAX_LENGTH)
    is_uniq = models.BooleanField('Уникальность поля', default=False)

    class Meta:
        verbose_name = 'атрибут'
        verbose_name_plural = 'Атрибуты'

    def __str__(self):
        return self.label


# class CardQuerySet(models.QuerySet):
#
#     def add_attrs_annotations(self):
#         return self.annotate(
#                     field_name=F('id_attribute__field_name'),
#                     attr_type=F('id_attribute__attr_type__attr_type'),
#                     label=F('id_attribute__label'),
#                     help_text=F('id_attribute__help_text'),
#                     is_uniq=F('id_attribute__is_uniq')
#                 )


class Card(models.Model):
    name = models.CharField('Имя', max_length=MAX_LENGTH)
    last_name = models.CharField('Фамилия', max_length=MAX_LENGTH)
    # objects = CardQuerySet.as_manager()

    class Meta:
        verbose_name = 'карточка'
        verbose_name_plural = 'Карточки'

    def __str__(self):
        return self.name


class CardAttributeQuerySet(models.QuerySet):

    def add_attrs_annotations(self):
        return self.select_related(
                    'id_attribute', 'id_attribute__attr_type'
                ).annotate(
                    field_name=F('id_attribute__field_name'),
                    attr_type=F('id_attribute__attr_type__attr_type'),
                    label=F('id_attribute__label'),
                    help_text=F('id_attribute__help_text'),
                    is_uniq=F('id_attribute__is_uniq')
                )


class CardAttribute(models.Model):
    id_attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, verbose_name='Атрибут',
        related_name='cards'
    )
    id_card = models.ForeignKey(
        Card, on_delete=models.CASCADE, verbose_name='Карточка',
        related_name='attrs'
    )
    value = models.TextField('Значение')
    objects = CardAttributeQuerySet.as_manager()

    class Meta:
        verbose_name = 'значение атрибута'
        verbose_name_plural = 'Значения атрибутов'

    def __str__(self):
        return '{} - {} - {}'.format(
            self.id_card, self.id_attribute, self.value)
