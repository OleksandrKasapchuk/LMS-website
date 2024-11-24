from django import forms
from .models import *


class CourseCreateForm(forms.ModelForm):
	class Meta:
		model = Course
		fields = ['name','cover']
		widjets = {
			"media": forms.FileInput()
		}


# class CommentCreateForm(forms.ModelForm):
# 	class Meta:
# 		model = Comment
# 		fields = ['content']