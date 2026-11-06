from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import CustomUser


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="test@mail.com", password="123qweQWE"
        )
        self.course = Course.objects.create(
            name="Test course", description="test course description", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="Test lesson",
            description="Test lesson description",
            video_link="https://www.youtube.com/",
            course=self.course,
        )
        self.client.force_authenticate(user=self.user)

        self.moderator = CustomUser.objects.create_user(
            email="moder@mail.com", password="123qweQWE"
        )
        group, _ = Group.objects.get_or_create(name="Модератор")
        self.moderator.groups.add(group)

    def test_lesson_retrieve(self):
        """тест подробности об уроке"""
        url = reverse("materials:lessons_retrieve", kwargs={"pk": self.lesson.pk})
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["name"], "Test lesson")
        self.assertEqual(data["description"], "Test lesson description")
        self.assertEqual(data["course"], self.course.pk)

    def test_lessons_list(self):
        """тест список уроков"""
        url = reverse("materials:lessons_list")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["results"][0]["name"], "Test lesson")
        self.assertEqual(data["results"][0]["description"], "Test lesson description")
        self.assertEqual(data["results"][0]["course"], self.course.pk)

    def test_lesson_create(self):
        """тест создание урока"""
        url = reverse("materials:lessons_create")
        data = {
            "name": "Test lesson",
            "description": "Test lesson description",
            "course": self.course.pk,
            "video_link": "https://www.youtube.com/",
        }

        response = self.client.post(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["name"], "Test lesson")
        self.assertEqual(data["description"], "Test lesson description")
        self.assertEqual(data["course"], self.course.pk)

    def test_lesson_update(self):
        """тест апдейт урока"""
        url = reverse("materials:lessons_update", kwargs={"pk": self.lesson.pk})
        data = {
            "name": "lesson Test",
        }
        response = self.client.patch(url, data=data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["name"], "lesson Test")

    def test_lesson_destroy(self):
        """тест удаление урока"""
        url = reverse("materials:lessons_destroy", kwargs={"pk": self.lesson.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_subscription(self):
        """тест на подписку"""
        url = reverse("materials:subscriptions_list")
        data = {"course": self.course.pk}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_lesson_permissions(self):
        """тесты на права модера"""
        self.client.force_authenticate(user=self.moderator)

        # модедратор дитейл урока
        url = reverse("materials:lessons_retrieve", kwargs={"pk": self.lesson.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # модератор апдейт урока
        url = reverse("materials:lessons_update", kwargs={"pk": self.lesson.pk})
        response = self.client.patch(url, data={"name": "Updated lesson"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # модератор создание урока
        url = reverse("materials:lessons_create")
        data = {
            "name": "Test lesson",
            "description": "Test description",
            "course": self.course.pk,
            "video_link": "https://www.youtube.com/",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # модератор удаление урока
        url = reverse("materials:lessons_destroy", kwargs={"pk": self.lesson.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
