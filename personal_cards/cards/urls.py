from django.conf import settings
# функция, позволяющая серверу отдавать файлы
from django.conf.urls.static import static
from django.urls import path

from .views import card_delete, card_edit, card_new, index

app_name = 'cards'


urlpatterns = [
    path('', index, name='index'),
    path('new_card/', card_new, name='card_new'),
    path('<int:card_id>/edit/', card_edit, name='card_edit'),
    path('<int:card_id>/delete/', card_delete, name='card_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
