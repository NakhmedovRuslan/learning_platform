from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import CustomUser


@shared_task
def deactivate_nonactive_users():
    """Бан пользователей которые не логинились месяц"""
    date = timezone.now() - timedelta(days=30)
    users = CustomUser.objects.all()

    for user in users:
        if user.last_login and user.last_login < date:
            user.is_active = False
            user.save()
