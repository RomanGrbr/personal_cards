from django.contrib import admin

from .models import Card, Value, Attribute, CardAttribute


admin.site.register(Card)
admin.site.register(Value)
admin.site.register(Attribute)
admin.site.register(CardAttribute)
