from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketPlaceView, TicketViewSet

router = DefaultRouter()
router.register(r'history', TicketViewSet)

urlpatterns = [
    path('place/', TicketPlaceView.as_view(), name='ticket_place'),
    path('', include(router.urls)),
]
