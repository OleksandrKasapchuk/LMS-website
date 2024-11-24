from django.urls import path
from .views import *

urlpatterns = [
	path('', IndexView.as_view(), name='index'),
	path('courses/', CourseView.as_view(), name='course-list'),
	path('courses/<int:pk>', CourseDetailView.as_view(), name='course-info'),
	path('create-course', CourseCreateView.as_view(), name='add-course'),
]