from django.urls import path

from .views import index, card_info

app_name = 'new_cards'


urlpatterns = [
    path('', index, name='list'),
    path('<int:card_id>', card_info, name='card_info'),
]
