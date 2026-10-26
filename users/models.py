from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    username = None
    city = models.CharField("Город", max_length=40, blank=True, null=True)
    phone = models.CharField("Номер телефона", max_length=15, blank=True, null=True)
    avatar = models.ImageField("Аватар", upload_to="avatars/", null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
