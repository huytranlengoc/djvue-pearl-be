from django.urls import path

from .views.auth import (CookieTokenLogoutView, CookieTokenObtainView,
                         CookieTokenRefreshView)
from .views.user import RegisterApiView

urlpatterns = [
    path("user/register", RegisterApiView.as_view(), name="register"),
    path("auth/token", CookieTokenObtainView.as_view(), name="login"),
    path("auth/refresh", CookieTokenRefreshView.as_view(), name="refresh"),
    path("auth/logout", CookieTokenLogoutView.as_view(), name="login"),
]
