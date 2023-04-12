from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from api.managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), max_length=255, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "dp_users"

    def __str__(self):
        return self.email
