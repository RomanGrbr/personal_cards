from django.db import models
from django.db.models import F
MAX_LENGTH = 100


class AttributeType(models.Model):
    type_name = models.CharField(
        'Тип атрибута (forms.fields)', max_length=MAX_LENGTH, unique=True
    )

    class Meta:
        ordering = ('type_name',)
        verbose_name = 'тип атрибута'
        verbose_name_plural = 'Типы атрибутов'

    def __str__(self):
        return self.type_name


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
        ordering = ('field_name',)
        verbose_name = 'атрибут'
        verbose_name_plural = 'Атрибуты'

    def __str__(self):
        return self.label


class Card(models.Model):
    first_name = models.CharField('Имя', max_length=MAX_LENGTH)
    last_name = models.CharField('Фамилия', max_length=MAX_LENGTH)
    avatar = models.ImageField(
        'Аватарка', upload_to='avatar/')

    class Meta:
        ordering = ('first_name',)
        verbose_name = 'карточка'
        verbose_name_plural = 'Карточки'

    def __str__(self):
        return self.first_name


class CardAttributeQuerySet(models.QuerySet):

    def add_attrs_annotations(self):
        return self.select_related(
                    'attribute', 'attribute__attr_type'
                ).annotate(
                    field_name=F('attribute__field_name'),
                    attr_type=F('attribute__attr_type__type_name'),
                    label=F('attribute__label'),
                    help_text=F('attribute__help_text'),
                    is_uniq=F('attribute__is_uniq')
                )


class CardAttribute(models.Model):
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, verbose_name='Атрибут'
    )
    card = models.ForeignKey(
        Card, on_delete=models.CASCADE, verbose_name='Карточка'
    )
    value = models.TextField('Значение')
    objects = CardAttributeQuerySet.as_manager()

    class Meta:
        default_related_name = 'card_attrs'
        verbose_name = 'значение атрибута'
        verbose_name_plural = 'Значения атрибутов'

    def __str__(self):
        return '{} - {} - {}'.format(
            self.card, self.attribute, self.value)
