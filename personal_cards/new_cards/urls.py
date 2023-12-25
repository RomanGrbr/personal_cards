from django.urls import path

from .views import index, card_info, card_edit, card_gallery, social_network
from .apps import NewCardsConfig

app_name = NewCardsConfig.name


urlpatterns = [
    path('', index, name='card_list'),
    path('<int:card_id>', card_info, name='card_info'),
    path('<int:card_id>/edit/', card_edit, name='card_edit'),
    path('<int:card_id>/gallery/', card_gallery, name='card_gallery'),
    path('<int:card_id>/social_network/', social_network, name='social_network'),
]
