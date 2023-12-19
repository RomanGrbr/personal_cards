from django.urls import path

from .views import (card_edit, card_new, index, card_gallery, card_info,
                    card_audio, )

app_name = 'cards'


urlpatterns = [
    path('', index, name='list'),
    path('new/', card_new, name='card_new'),
    path('<int:card_id>', card_info, name='card_info'),
    path('<int:card_id>/edit/', card_edit, name='card_edit'),
    path('<int:card_id>/gallery/', card_gallery, name='card_gallery'),
    path('<int:card_id>/audio/', card_audio, name='card_audio'),
]
