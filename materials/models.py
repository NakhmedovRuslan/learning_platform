from django.db import models

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.CharField(max_length=300, verbose_name="Описание")
    preview = models.ImageField(upload_to="course_previews/", verbose_name="Превью")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["name"]


class Lesson(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс")
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.CharField(max_length=300, verbose_name="Описание")
    preview = models.ImageField(upload_to="lesson_previews/", verbose_name="Превью")
    video_link = models.URLField(verbose_name="Ссылка на видео")

    def __str__(self):
        return f"{self.course.name} — {self.name}"

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['course', 'name']
