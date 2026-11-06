from django.db import models

from users.models import CustomUser


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.CharField(max_length=300, verbose_name="Описание")
    preview = models.ImageField(
        upload_to="course_previews/", verbose_name="Превью", blank=True, null=True
    )
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="Создатель курса"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["name"]


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс"
    )
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.CharField(max_length=300, verbose_name="Описание")
    preview = models.ImageField(
        upload_to="lesson_previews/", verbose_name="Превью", blank=True, null=True
    )
    video_link = models.URLField(verbose_name="Ссылка на видео", blank=True, null=True)

    def __str__(self):
        return f"{self.course.name} — {self.name}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["course", "name"]


class Subscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} — {self.course}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
