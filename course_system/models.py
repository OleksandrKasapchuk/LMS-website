from django.db import models
from auth_system.models import *


class Course(models.Model):
	name = models.CharField(max_length=100)
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	cover = models.ImageField(upload_to="course_media", null=True,blank=True)

	def __str__(self):
		return f"{self.name} - {self.user}"

class Lesson(models.Model):
	name = models.CharField(max_length=50)
	content = models.TextField()
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	upload_data = models.FileField(upload_to="lesson_media", null=True, blank=True)

	def __str__(self):
		return f"{self.name} -  {self.course}"