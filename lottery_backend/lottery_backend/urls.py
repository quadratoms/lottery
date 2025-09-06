"""
URL configuration for lottery_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("accounts.urls")),
    path("api/v1/payments/", include("payments.urls")),
    path("api/v1/kyc/", include("kyc.urls")),
    path("api/v1/games/", include("games.urls")),
    path("api/v1/draws/", include("draws.urls")),
    path("api/v1/tickets/", include("tickets.urls")),
    path("api/v1/payouts/", include("payouts.urls")),
    path("api/v1/wallet/", include("wallet.urls")),
    path("api/v1/adminpanel/", include("adminpanel.urls")),
    path("api/v1/audit/", include("audit.urls")),
    path("api/v1/notifications/", include("notifications.urls")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
