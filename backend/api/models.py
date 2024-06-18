import uuid

from django.db import models
from django.db.models import F
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.fields import JSONField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from api.constants import (AUDIO, CHECKBOX, DATE, DATE_TIME, EMAIL, FILE,
                           IMAGE, MOVE, NUMBER, STRING, TEL, TEXT, TIME, URL,
                           WEEK)


class PerObj(models.Model):
    """Персональные карточки."""
    pass


class ScsPage(models.Model):
    """Страницы социальных сетей."""
    pass


class Post(models.Model):
    """Публикации в социальных сетях."""
    pass


class SmiNews(models.Model):
    """Средства массовой информации (СМИ)."""
    pass


class MmdMedia(models.Model):
    """Медиа"""
    pass


class MmdJSON(models.Model):
    """JSON"""
    pass


class TypeNames:
    choices = (
        (NUMBER, 'Число'),
        (TEXT, 'Строка'),
        (STRING, 'Текст'),
        (DATE, 'Дата'),
        (WEEK, 'Неделя'),
        (DATE_TIME, 'Дата и время'),
        (TIME, 'Время'),
        (EMAIL, 'Электронная почта'),
        (FILE, 'Файл'),
        (IMAGE, 'Фото'),
        (MOVE, 'Видео'),
        (AUDIO, 'Аудио'),
        (CHECKBOX, 'Чекбокс'),
        (URL, 'Ссылка'),
        (TEL, 'Телефон')
    )


class AttributeType(models.Model):
    """Типы атрибутов."""

    type_name = models.CharField(
        max_length=250,
        choices=TypeNames.choices,
        default=TEXT,
        verbose_name='Тип атрибута (text, integer, file...)',
        unique=True
        )

    class Meta:
        ordering = ('type_name',)
        verbose_name = 'тип атрибута'
        verbose_name_plural = 'Типы атрибутов'

    def __str__(self):
        return self.type_name


class Attribute(models.Model):
    """Атрибуты."""

    field_name = models.SlugField('Имя поля', unique=True)
    attr_type = models.ForeignKey(
        AttributeType, on_delete=models.PROTECT, related_name='attributes',
        verbose_name='Тип атрибута (поля)'
    )
    label = models.CharField(
        'Название поля (label)', max_length=250)
    help_text = models.CharField(
        'Текст подсказка (help_text)', max_length=250)
    is_uniq = models.BooleanField('Уникальность поля', default=False)

    class Meta:
        ordering = ('field_name',)
        verbose_name = 'атрибут'
        verbose_name_plural = 'Атрибуты'

    def __str__(self):
        return self.label


class Card(models.Model):
    """Карточка персоны."""

    card_uuid = models.UUIDField(
        'Уникальный идентификатор карточки uuid',
        default=uuid.uuid4, editable=False, unique=True
    )
    full_name = models.CharField(
        'ФИО персоны', max_length=250, unique=True)
    avatar = models.ImageField(
        'Аватарка', upload_to='avatar/', null=True, blank=True)
    auto_collect = models.BooleanField('Автоматический сбор', default=False)
    # search_vector = SearchVectorField(null=True)

    class Meta:
        verbose_name = 'карточка персоны'
        verbose_name_plural = 'Карточки персон'
        ordering = ('full_name',)
        # indexes = [GinIndex(fields=['search_vector'])]

    def __str__(self):
        return self.full_name


class SocialNetwork(models.Model):
    """Страница в социальной сети."""

    card = models.ForeignKey(
        Card, on_delete=models.CASCADE,
        verbose_name='Карточка', related_name='social_networks',
    )
    social_id = models.CharField(
        'socialId страницы из scs_page', db_index=True, max_length=100)

    class Meta:
        verbose_name = 'персональная страница в социальной сети'
        verbose_name_plural = 'Персональные страницы в социальных сетях'
        unique_together = ('card', 'social_id')

    def __str__(self):
        return '{}: {}'.format(self.card, self.social_id)


class CardAttributeQuerySet(models.QuerySet):
    """Аннотация для CardAttribute."""

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
    """Значения атрибутов."""

    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, verbose_name='Атрибут',
    )
    card = models.ForeignKey(
        Card, on_delete=models.CASCADE, verbose_name='Карточка',
    )
    value = models.TextField('Значение')
    confirmed = models.BooleanField('Подтвержден', default=False)
    vector_base = models.TextField('Вектор', blank=True)
    objects = CardAttributeQuerySet.as_manager()

    class Meta:
        default_related_name = 'attrs'
        verbose_name = 'значение атрибута'
        verbose_name_plural = 'Значения атрибутов'
        ordering = ('attribute',)

    def __str__(self):
        return '{} - {} - {}'.format(
            self.card, self.attribute, self.value)
