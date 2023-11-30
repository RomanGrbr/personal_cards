from django.contrib import admin

from .models import Card, AttributeType, Attribute, CardAttribute


admin.site.register(Card)
admin.site.register(AttributeType)
admin.site.register(Attribute)
admin.site.register(CardAttribute)
