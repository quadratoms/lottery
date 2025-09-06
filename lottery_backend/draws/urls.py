from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DrawViewSet

router = DefaultRouter()
router.register(r'draws', DrawViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
