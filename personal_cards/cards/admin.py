from django.contrib import admin

from .models import Attribute, AttributeType, Card, CardAttribute

admin.site.register(Card)
admin.site.register(AttributeType)
admin.site.register(Attribute)
admin.site.register(CardAttribute)
