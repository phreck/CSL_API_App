from django.urls import path, include
from rest_framework import routers
from .views import (
    ScreeningEntityViewSet,
    AddressViewSet,
    EntityIDViewSet,
    SearchQueryViewSet
)

router = routers.DefaultRouter()
router.register(r'entities', ScreeningEntityViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'entity-ids', EntityIDViewSet)
router.register(r'search-history', SearchQueryViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]