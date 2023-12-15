from django.urls import path

from .views import (card_delete, card_edit, card_new, index, card_info,
                    card_gallery,
                    )

app_name = 'cards'


urlpatterns = [
    path('', index, name='index'),
    path('new/', card_new, name='card_new'),
    path('<int:card_id>', card_info, name='card_info'),
    path('<int:card_id>/edit/', card_edit, name='card_edit'),
    path('<int:card_id>/delete/', card_delete, name='card_delete'),
    path('<int:card_id>/gallery/', card_gallery, name='card_gallery'),
]
