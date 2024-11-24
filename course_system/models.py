from django.db import models
from auth_system.models import *


class Course(models.Model):
	name = models.CharField(max_length=100)
	owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	cover = models.ImageField(upload_to="course_media", null=True,blank=True)


class Lesson(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	content = models.TextField()