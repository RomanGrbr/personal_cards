from django.conf import settings
# функция, позволяющая серверу отдавать файлы
from django.conf.urls.static import static
from django.urls import path

from .views import new_card, index, card_edit, card_delete, card_attr_delete

app_name = 'cards'


urlpatterns = [
    path('', index, name='index'),
    path('new_card/', new_card, name='new_card'),
    # path('new_card/<str:field_name>', new_card, name='new_card'),
    path('<int:card_id>/edit/', card_edit, name='card_edit'),
    path('<int:card_id>/delete/', card_delete, name='card_delete'),
    path('card_attr_delete/<int:field_id>/delete/', card_attr_delete, name='card_attr_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
