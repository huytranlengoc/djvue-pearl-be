# Create a virtual environment

```python
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
```

# Install Django

```python
pip install django==4.2
pip install djangorestframework==3.14.0
```

# Start a new project

```python
django-admin startproject core .
```

Structure:

```
├── core
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```

# Prepare setting files

Update file `core/settings.py`

```
import os
SECRET_KEY = os.environ.get("SECRET_KEY", "djvue-secret-key")
DEBUG = bool(int(os.environ.get("DEBUG", "1")))
```

Change settings to multiple environment files:

```bash
mkdir -p core/settings
mv core/settings.py core/settings/base.py
touch core/settings/__init__.py
touch core/settings/{development,test,staging,production}.py
echo "from .base import *  # noqa" >> core/settings/{development,test,staging,production}.py
```

Update file `core/settings/base.py` (add `.parent`)

```
BASE_DIR = Path(__file__).resolve().parent.parent.parent
```

Update `DJANGO_SETTINGS_MODULE` in file `manage.py`

```
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.development")
```

# Split installed apps

Update file `core/settings/base.py` like this:

```
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
]

LOCAL_APPS = [
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
```

# Split dependencies for pip

```
mkdir -p requirements
touch requirements/{base,dev,test,prod}.txt
echo "-r base.txt" >! requirements/{dev,test,prod}.txt
echo "-r requirements/dev.txt" >! requirements.txt
echo "-r requirements/prod.txt" >! requirements_prod.txt
pip freeze >! requirements/base.txt
```

# Create a new app named `api`

```
./manage.py startapp api
```

Update `core/settings/base.py`:

```
LOCAL_APPS = [
  "api",
]
```

# Create a common model

```
mkdir -p api/models
mv api/models.py api/models/base.py
echo "from .base import BaseModel" >! api/models/__init__.py
```

Update `api/models/base.py`:

```
from django.conf import settings
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        default=None,
        blank=True,
        editable=False,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created_by",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        default=None,
        blank=True,
        editable=False,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated_by",
    )

    class Meta:
        abstract = True

```

* We add some common fields: `created_at`, `updated_at`, `created_by`, `updated_by` to track history of each record

# Create User model to customize default AUTH_USER_MODEL

Add `managers` folder to `api`:

```
mkdir -p api/managers
echo "from .user import UserManager" > api/managers/__init__.py
touch api/managers/user.py

```

Add the following content to `api/managers/user.py`:

```
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)

```

Add `User` model:

```
echo "from .user import User" >> api/models/__init__.py
touch api/models/user.py
```

Add the following content to `api/models/user.py`:

```
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from api.managers import UserManager


class User(AbstractUser):
    uuid = models.UUIDField(
        primary_key=True, db_index=True, default=uuid.uuid4, unique=True, editable=False
    )

    username = None
    email = models.EmailField(_("email address"), max_length=255, unique=True)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email

```

Add the followint contents to `core/settings/base.py`:

```
# Customize user model
AUTH_USER_MODEL = "api.User"
```

From now, we can make migrations and migrate.

```
./manage.py makemigrations
./manage.py migrate
```

Create a testcase by adding the following content to `api/tests.py`:

```
from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", password="foo")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser("super@user.com", "foo")
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False
            )

```

At this point, we can run a simple test:

```
./manage.py test api
```

# Add User to Admin Site

Add new file `api/forms.py`:

```
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ("email", "first_name", "last_name")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")
```

Add the following contents to `apis/admin.py`:

```
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    # when display the user model in the admin panel, the following fields are shown
    list_display = ["email", "first_name", "last_name", "is_staff", "is_active"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )

    # when creating a new user, the password fields are shown
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = [
        "email",
        "first_name",
        "last_name",
    ]
    ordering = ["email", "first_name", "last_name"]
    filter_horizontal = []


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)

```

# Add simple jwt

Add `djangorestframework-simplejwt` to pip

```
echo "djangorestframework-simplejwt==5.2.2" >> requirements/base.txt
pip install -r requirements.txt
```

Update the following content to `core/settings/base.py`:

```
THIRD_PARTY_APPS = [
    ...
    "rest_framework_simplejwt",
]

# Configure for DRF
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("api.authentications.JWTCookieAuthentication",)
}

# Configure for JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
}
JWT_AUTH_COOKIE = "refresh"
```

Add new file `api/serializers/auth.py`:

```
from django.conf import settings
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from rest_framework_simplejwt.tokens import RefreshToken


class CookieTokenObtainSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email", "")
        password = data.get("password", "")

        if email and password:
            user = authenticate(email=email, password=password)
            # check valid credentials
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise exceptions.ValidationError(msg)
            # check user status
            if not user.is_active:
                msg = _("User account is disabled.")
                raise exceptions.ValidationError(msg)
            # valid user
            refresh = RefreshToken.for_user(user)
            data = dict(
                refresh=str(refresh),
                access=str(refresh.access_token),
            )
        else:
            msg = _("Must include 'email' and 'password'.")
            raise exceptions.ValidationError(msg)
        return data


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField(required=False)

    def extract_refresh_token(self):
        request = self.context["request"]
        # Override token extraction to allow for refresh token in request body
        if "refresh" in request.data and request.data["refresh"]:
            return request.data["refresh"]
        # Default with refresh token in HttpOnly cookie
        cookie_name = settings.JWT_AUTH_COOKIE
        if cookie_name and cookie_name in request.COOKIES:
            return request.COOKIES[cookie_name]
        else:
            raise InvalidToken("No valid token found")

    def validate(self, attrs):
        # validates and isused to build a new JWT
        refresh = RefreshToken(self.extract_refresh_token())

        data = {"access": str(refresh.access_token)}
        if jwt_settings.ROTATE_REFRESH_TOKENS:
            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()
        data["refresh"] = str(refresh)
        return data

```

Add new file `api/views/auth.py`:

```
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from api.authentications import set_refresh_cookie, unset_refresh_cookie
from api.serializers import (CookieTokenObtainSerializer,
                             CookieTokenRefreshSerializer)


class CookieTokenObtainView(TokenObtainPairView):
    """
    Same as rest_framework_simplejwt.views.TokenObtainPairView but:
        * set HttpOnly cookie to store refresh token
        * remove `refresh` from response data.
    """

    serializer_class = CookieTokenObtainSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == status.HTTP_200_OK and "refresh" in response.data:
            set_refresh_cookie(response, response.data["refresh"])
            del response.data["refresh"]
        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):
    """
    Override from rest_framework_simplejwt.views.TokenRefreshView:
        * set HttpOnly cookie to store refresh token
        * remote `refresh` from response data.
    """

    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == status.HTTP_200_OK and "refresh" in response.data:
            set_refresh_cookie(response, response.data["refresh"])
            del response.data["refresh"]
        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenLogoutView(APIView):
    def post(self, request):
        response = Response()
        unset_refresh_cookie(response)
        response.data = {
            "detail": _("You have been successfully logged out."),
        }
        return response

```

Add new file `api/authentications.py`

```
from django.conf import settings
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from rest_framework_simplejwt.tokens import RefreshToken


def set_refresh_cookie(response, refresh_token):
    cookie_name = settings.JWT_AUTH_COOKIE
    token_expiration = timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME
    response.set_cookie(
        cookie_name,
        value=refresh_token,
        expires=token_expiration,
        httponly=True,
        samesite="None",
        secure=True,
    )


def unset_refresh_cookie(response):
    response.delete_cookie(settings.JWT_AUTH_COOKIE)


class JWTCookieAuthentication(JWTAuthentication):
    def authenticate(self, request):
        cookie_name = settings.JWT_AUTH_COOKIE
        header = self.get_header(request)
        if header is None:
            raw_token = request.COOKIES.get(cookie_name)
        else:
            raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        # get token from refresh cookie
        refresh = RefreshToken(raw_token)
        validated_token = refresh.access_token
        return self.get_user(validated_token), validated_token

```

Functions:
* `CookieTokenRefreshSerializer`: override `validate` to get refresh token from request body or cookie
    * `refresh`: set required to false, because it's optional
    * `extract_refresh_token`: get refresh token from request body or cookie
    * `validate`: validate refresh token and return new access token and refresh token (override from library)
* `CookieTokenRefreshView`:
    * override `finalize_response` to set refresh token to HTTP Cookie
    * delete refresh token from response
* `CookieTokenObtainView`:
    * Customize login functions based on `rest_framework_simplejwt.views.TokenObtainPairView ` but do set cookie on response
    * Use `RefreshToken.for_user()` to generate refresh token

Add new file `api/urls.py`:

```
from django.urls import path

from .views.auth import (CookieTokenLogoutView, CookieTokenObtainView,
                         CookieTokenRefreshView)

urlpatterns = [
    path("auth/token", CookieTokenObtainView.as_view(), name="login"),
    path("auth/refresh", CookieTokenRefreshView.as_view(), name="refresh"),
    path("auth/logout", CookieTokenLogoutView.as_view(), name="logout"),
]

```

Add the following content to `core/urls.py`:

```
from django.urls import path, include

path('api/', include('api.urls')),

```

You can know create a super user , then call to these 2 api to get access token and refresh token.

```bash
./manage.py createsuperuser
```

Example input: `admin@example.com` / `admin`

Sample call:
* [Request to access token](./docs/how_to_use_httpie.md#login)
* [Request to refresh token](./docs/how_to_use_httpie.md#register-new-user)

# Add Register API

Add User Serializer:

```
mkdir -p api/serializers
touch api/serializers/__init__.py
touch api/serializers/user.py
echo "from .user import UserSerializer" >> api/serializers/__init__.py
```

Add the following content to `api/serializers/user.py`:

```
from rest_framework.serializers import ModelSerializer
from api.models import User

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            password = validated_data.pop('password', None)
            instance = self.Meta.model(**validated_data)
            if password is not None:
                instance.set_password(password)
            instance.save()
            return instance

```

Add Register api view:

```
mkdir -p api/views
rm -f api/views.py
touch api/views/__init__.py
touch api/views/user.py
echo "from .user import RegisterApiView" >> api/views/__init__.py
```

Add the following content to `api/views/user.py`:

```
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import UserSerializer


class RegisterApiView(APIView):
    def post(self, request):
        data = request.data
        if data["password"] != data["password_confirm"]:
            raise exceptions.APIException("Passwords must match")

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

```

Add register url to `api/urls.py`:

```
from .views import RegisterApiView

urlpatterns = [
    ...
    path("register", RegisterApiView.as_view(), name="register"),
]
```

You can register new user by request to this api now, sample call:
[Request to RegisterAPI](./docs/how_to_use_httpie.md#register-new-user)
