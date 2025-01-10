from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
	avatar = models.ImageField(upload_to="avatars",default="../static/images/default_avatar.jpg", null=True, blank=True)

	def __str__(self):
		return self.username