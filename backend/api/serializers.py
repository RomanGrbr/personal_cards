from collections import Counter

from rest_framework import serializers

from pkt_fpk.settings import MEDIA_URL
from .constants import AUDIO, FILE, IMAGE, MOVE
from .models import Attribute, Card, CardAttribute, SocialNetwork
from .utils import get_image


class Base64ImageField(serializers.ImageField):
    """Кастомное поле изображения"""

    def to_representation(self, value):
        return str(MEDIA_URL + value.name)

    def to_internal_value(self, data):
        data = get_image(data)
        return super(Base64ImageField, self).to_internal_value(data)

class AttributeSerializer(serializers.ModelSerializer):
    attr_type = serializers.SlugRelatedField(
        slug_field='type_name', read_only=True)

    class Meta:
        model = Attribute
        fields = '__all__'


class SocialNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialNetwork
        fields = '__all__'


class CardAttributeSerializer(serializers.ModelSerializer):
    field_name = serializers.ReadOnlyField()
    attr_type = serializers.ReadOnlyField()
    label = serializers.ReadOnlyField()
    help_text = serializers.ReadOnlyField()
    is_uniq = serializers.BooleanField(read_only=True)

    class Meta:
        model = CardAttribute
        fields = '__all__'


class CardSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(use_url=False)
    confirm_scs = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = ('id', 'full_name', 'avatar', 'auto_collect', 'confirm_scs')

    def get_confirm_scs(self, obj):
        return obj.social_networks.exists()

    def validate(self, data):
        uniq_attrs = Attribute.objects.filter(is_uniq=True)
        attrs = self.initial_data.get('attrs')
        count_attrs = dict(Counter([attr['id'] for attr in attrs]))
        for attr in uniq_attrs:
            if count_attrs.get(attr.id, 0) > 1:
                raise serializers.ValidationError(
                    '{} должно быть уникальным'.format(attr))
        return data

    @staticmethod
    def create_attrs(attrs, card):
        attrs_list = list()
        for attr in attrs:
            attr_obj = Attribute.objects.get(id=attr.get('id'))
            value = attr.get('value')
            attrs_list.append(CardAttribute(
                card=card,
                attribute=attr_obj,
                value=value
            ))
        attrs_list.sort(key=(lambda item: item.attribute.field_name),
                        reverse=True)
        CardAttribute.objects.bulk_create(attrs_list)

    def create(self, validated_data):
        card = Card.objects.create(**validated_data)
        if self.initial_data.get('attrs'):
            try:
                attrs = self.initial_data.pop('attrs')
                self.create_attrs(attrs, card)
            except:
                # Удалить новую карточку при ошибке записи атрибутов
                card.delete()
                raise serializers.ValidationError(
                    'Проверьте корректность заполнения атрибутов')
        return card

    def update(self, instance, validated_data):
        if self.initial_data.get('attrs'):
            # Сохранить старые атрибуты
            # для восстановления при ошибке записи новых.
            last_attrs = [
                {
                    'value': obj.value,
                    'id': obj.attribute.id
                    } for obj in instance.attrs.all()
                ]
            instance.attrs.exclude(attribute__attr_type__type_name__in=[
                IMAGE, AUDIO, MOVE, FILE]).delete()
            try:
                self.create_attrs(self.initial_data.pop('attrs'), instance)
            except:
                # Восстановить старые атрибуты при ошибке записи новых
                self.create_attrs(last_attrs, instance)
                raise serializers.ValidationError(
                    'Проверьте корректность заполнения атрибутов'
                )
        return super().update(instance, validated_data)
