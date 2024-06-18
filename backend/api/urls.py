from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AttributeViewSet, CardAttributeViewSet, CardViewSet,
                    maclabel, social_search, wiki_search)

app_name = 'api'

router = DefaultRouter()
router.register('cards', CardViewSet, basename='cards')
router.register('cardattrs', CardAttributeViewSet, basename='cardattrs')
router.register('attrs', AttributeViewSet, basename='attrs')

urlpatterns = [
    path('', include(router.urls)),
    path('wiki_search/', wiki_search, name='wiki_search'),
    path('maclabel/', maclabel, name='maclabel'),
    path('social_search/', social_search, name='social_search'),
    
]
