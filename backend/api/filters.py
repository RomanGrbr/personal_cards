from django_filters.rest_framework import CharFilter, FilterSet

from .models import Attribute, CardAttribute


class CardAttributeFilter(FilterSet):
    attr_type = CharFilter(
        field_name='attribute__attr_type__type_name',
        lookup_expr='exact',
        label='Тип атрибута')
    card = CharFilter(
        field_name='card__id',
        lookup_expr='exact',
        label='Карточка')

    class Meta:
        model = CardAttribute
        fields = ('attr_type', 'card')


class AttributeFilter(FilterSet):
    attr_type = CharFilter(
        field_name='attr_type__type_name',
        lookup_expr='exact',
        label='Тип атрибута')

    class Meta:
        model = Attribute
        fields = ('attr_type',)
