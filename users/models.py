from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField("Имя", max_length=100, null=False, blank=False)
    last_name = models.CharField("Фамилия", max_length=100, null=False, blank=False)
    city = models.CharField("Город", max_length=40, blank=True, null=True)
    phone = models.CharField("Номер телефона", max_length=15, blank=True, null=True)
    avatar = models.ImageField("Аватар", upload_to="avatars/", null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


