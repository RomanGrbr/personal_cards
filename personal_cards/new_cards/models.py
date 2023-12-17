from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q, F
from django.db.models import Exists, OuterRef

MAX_LENGTH = 250


# class CardQuerySet(models.QuerySet):
#
#     def attr_annotations(self):
#         return self.attrs.all().select_related('attribute', 'value').annotate(
#             field_name=F('attribute__field_name'),
#             label=F('attribute__label'),
#             help_text=F('attribute__help_text'),
#             is_uniq=F('attribute__is_uniq'),
#         )


class Card(models.Model):
    name = models.CharField('Имя', max_length=MAX_LENGTH)
    last_name = models.CharField('Фамилия', max_length=MAX_LENGTH)
    # objects = CardQuerySet.as_manager()

    class Meta:
        verbose_name = 'карточка'
        verbose_name_plural = 'Карточки'

    def __str__(self):
        return self.name


class Value(models.Model):
    text = models.CharField(
        'Текст', max_length=MAX_LENGTH, blank=True, null=True)
    integer = models.IntegerField('Число', blank=True, null=True)
    image = models.ImageField(
        'Изображение', upload_to='new_cards/', blank=True, null=True)

    class Meta:
        verbose_name = 'значение атрибута'
        verbose_name_plural = 'Значения атрибутов'
        constraints = [
            models.CheckConstraint(
                check=(
                          Q(text__isnull=True) &
                          Q(integer__isnull=False) &
                          Q(image__isnull=False)
                      ) | (
                            Q(text__isnull=False) &
                            Q(integer__isnull=True) &
                            Q(image__isnull=False)
                      ) | (
                            Q(text__isnull=False) &
                            Q(integer__isnull=False) &
                            Q(image__isnull=True)
                      ),
                name='only_one_value',
            )
        ]

    def __str__(self):
        for field in self._meta.get_fields():
            if field.name not in ['id', 'cards'] and getattr(self, field.name):
                return f'{getattr(self, field.name)}'
        return super().__str__()


class Attribute(models.Model):
    field_name = models.CharField(
        'Имя поля', max_length=MAX_LENGTH, unique=True)
    label = models.CharField(
        'Название поля (label)', max_length=MAX_LENGTH, unique=True)
    help_text = models.CharField(
        'Текст подсказка (help_text)', max_length=MAX_LENGTH)
    is_uniq = models.BooleanField('Уникальность поля', default=False)

    class Meta:
        verbose_name = 'тип атрибута'
        verbose_name_plural = 'Типы атрибутов'

    def __str__(self):
        return self.label


class CardQuerySet(models.QuerySet):

    def attr_annotations(self):
        return self.select_related('attribute', 'value').annotate(
            field_name=F('attribute__field_name'),
            label=F('attribute__label'),
            help_text=F('attribute__help_text'),
            is_uniq=F('attribute__is_uniq'),
        )


class CardAttribute(models.Model):
    card = models.ForeignKey(
        Card, on_delete=models.CASCADE, verbose_name='Карточка',
        related_name='attrs'
    )
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, verbose_name='Атрибут',
        related_name='cards'
    )
    value = models.ForeignKey(
        Value, on_delete=models.CASCADE, verbose_name='Значение',
        related_name='cards'
    )
    objects = CardQuerySet.as_manager()

    class Meta:
        verbose_name = 'атрибут'
        verbose_name_plural = 'атрибуты'
        # constraints = [
        #     models.UniqueConstraint(fields=['card_id', 'attribute_id'],
        #                             name='unique_attr_type'),
        # ]

    def clean(self):
        if CardAttribute.objects.filter(
                card=self.card, attribute=self.attribute
        ).exists():
            raise ValidationError(
                'У карточки может быть только один атрибут указанного типа')
        return super().save(self)

    def __str__(self):
        return f'{self.card.name} - {self.attribute.label}'
