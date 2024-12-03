from django.db import models
from auth_system.models import *
import random
import string


class Course(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to="course_media", null=True, blank=True)
    code = models.CharField(max_length=6, unique=True, blank=True)  # Унікальний код

    def __str__(self):
        return f"{self.name} - {self.user}"

    def save(self, *args, **kwargs):
        if not self.code:  # Генеруємо код лише, якщо його ще немає
            self.code = self._generate_unique_code()
        super().save(*args, **kwargs)

    def _generate_unique_code(self):
        """Генерує унікальний 6-символьний код."""
        while True:
            code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            if not Course.objects.filter(code=code).exists():
                return code


class Lesson(models.Model):
	name = models.CharField(max_length=50)
	content = models.TextField()
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	upload_data = models.FileField(upload_to="lesson_media", null=True, blank=True)

	def __str__(self):
		return f"{self.name} -  {self.course}"


class Subscription(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="subscriptions")
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="subscribers")
	subscribed_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ("user", "course")  # Уникальна підписка для кожної пари користувач-курс

	def __str__(self):
		return f"{self.user} підписався на {self.course}"