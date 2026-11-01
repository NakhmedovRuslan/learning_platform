from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError

from materials.models import Course, Lesson

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    objects = CustomUserManager()
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


class Payments(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = "cash", "Наличными"
        CARD = "card", "Картой"


    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(choices=PaymentMethod.choices, max_length=20)

    def clean(self):
        super().clean()

        if bool(self.course) == bool(self.lesson):
            raise ValidationError(
                "Необходимо указать либо курс, либо отдельный урок."
            )

    def __str__(self):
        return f"Пользователь {self.user.email} сделал платёж №{self.pk} на сумму {self.payment_amount}. \nОплатил {self.course or self.lesson} {self.payment_method}."

