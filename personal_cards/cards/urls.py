from django.urls import path

from .views import (card_edit,
                    card_new,
                    index,
                    card_gallery,
                    card_info_or_delete,
                    CardListView,
                    )

app_name = 'cards'


urlpatterns = [
    # path('', CardListView.as_view(), name='list'),
    path('', index, name='list'),
    path('new/', card_new, name='card_new'),
    # path('new/', CardCreateView.as_view(), name='card_new'),
    path('<int:card_id>', card_info_or_delete, name='card_info_or_delete'),
    path('<int:card_id>/edit/', card_edit, name='card_edit'),
    path('<int:card_id>/gallery/', card_gallery, name='card_gallery'),
]
