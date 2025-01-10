from django.db import models
from auth_system.models import *
from django.utils.timezone import now
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
        if not self.code:  # Генерує код лише, якщо його ще немає
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

    date_published = models.DateTimeField(auto_now_add=True)
    date_to = models.DateTimeField(blank=True, null=True)

    edited = models.BooleanField(default=False)  # Поле для відстеження редагування
    last_edited_at = models.DateTimeField(null=True, blank=True)  # Дата останнього редагування
    
    max_mark = models.PositiveIntegerField(default=100)

    def save(self, *args, **kwargs):
        # Перевіряємо, чи це оновлення існуючого об'єкта
        if self.pk is not None:
            original = Lesson.objects.get(pk=self.pk)
            # Якщо будь-яке поле змінено, встановлюємо прапорець "edited" і час
            if original.name != self.name or original.content != self.content or original.date_to != self.date_to:
                self.edited = True
                self.last_edited_at = now()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} - {self.course}"
    
    def get_user_answer(self, user):
        return self.answers.filter(user=user).first()


class Subscription(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="subscriptions")
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="subscribers")
	subscribed_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ("user", "course")  # Уникальна підписка для кожної пари користувач-курс

	def __str__(self):
		return f"{self.user} підписався на {self.course}"


class Comment(models.Model):
	content = models.CharField(max_length=100)
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comments")
	lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="comments")
	date_published = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user} - {self.date_published}"
	
	class Meta:
		ordering = ('-date_published',)


class Answer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="answers")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="answers")
    date_published = models.DateTimeField(auto_now_add=True)
    mark = models.IntegerField(null=True, blank=True)
    user_send = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user} - {self.lesson} - {self.date_published}"


class UploadedFile(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="answer_media")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for {self.answer}: {self.file.name}"