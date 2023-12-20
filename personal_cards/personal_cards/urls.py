from django.conf import settings
# функция, позволяющая серверу отдавать файлы
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('cards/', include('cards.urls')),
    path('new_cards/', include('new_cards.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
