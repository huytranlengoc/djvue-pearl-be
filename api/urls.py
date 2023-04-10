from django.urls import path

from api.views import CookieTokenObtainPairView, CookieTokenRefreshView

from .views import RegisterApiView

urlpatterns = [
    path("register", RegisterApiView.as_view(), name="register"),
    path("token", CookieTokenObtainPairView.as_view(), name="token"),
    path("token/refresh", CookieTokenRefreshView.as_view(), name="refresh"),
]
