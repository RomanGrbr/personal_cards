from django.urls import path

from .views import index, card_info, card_edit
from .apps import NewCardsConfig

app_name = NewCardsConfig.name


urlpatterns = [
    path('', index, name='card_list'),
    path('<int:card_id>', card_info, name='card_info'),
    path('<int:card_id>/edit/', card_edit, name='card_edit'),
]
