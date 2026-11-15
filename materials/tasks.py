from celery import shared_task
from django.core.mail import send_mail

from config import settings
from materials.models import Subscription


@shared_task
def send_mail_update_course(course_id):
    """Отправка email подписчикам курса после его обновления"""
    subscriptions = Subscription.objects.filter(course_id=course_id)

    for subscription in subscriptions:
        send_mail(
            subject="Обновление материалов курса",
            message=f"Курс {subscription.course.name} обновлен",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[subscription.user.email],
        )
