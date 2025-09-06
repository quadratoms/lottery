from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GameConfigViewSet, OddsSchemeViewSet

router = DefaultRouter()
router.register(r'gameconfigs', GameConfigViewSet)
router.register(r'oddsschemes', OddsSchemeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
