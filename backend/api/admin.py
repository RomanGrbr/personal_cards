from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (Attribute, AttributeType, Card, CardAttribute,
                     SocialNetwork)


@admin.register(AttributeType, Attribute, CardAttribute, SocialNetwork)
class MyAdmin(admin.ModelAdmin):
    pass


class CardAttrAdmin(admin.TabularInline):
    model = CardAttribute
    extra = 1


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):

    list_display = ('full_name', 'count_pages', 'get_avatar')
    readonly_fields = ('count_pages',)
    inlines = (CardAttrAdmin,)

    def count_pages(self, obj):
        return obj.social_networks.count()

    count_pages.short_description = 'Количество страниц'

    def get_avatar(self, obj):
        if obj.avatar:
            return mark_safe(
                '<img src={} width="80" height="60">'.format(obj.avatar.url)
            )
        return None

    get_avatar.short_description = "Аватарка"
