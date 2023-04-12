from django.urls import path

from api.views import CookieTokenRefreshView

from .views import LoginApiView, RegisterApiView

urlpatterns = [
    path("login", LoginApiView.as_view(), name="login"),
    path("register", RegisterApiView.as_view(), name="register"),
    path("refresh", CookieTokenRefreshView.as_view(), name="refresh"),
]
