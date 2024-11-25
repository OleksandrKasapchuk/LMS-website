from django.urls import path
from .views import *


urlpatterns = [
	path('', IndexView.as_view(), name='index'),
	path('courses/', CourseView.as_view(), name='course-list'),
	path('create-course', CourseCreateView.as_view(), name='add-course'),
	path('courses/<int:pk>', CourseDetailView.as_view(), name='course-info'),
	path('edit-course/<int:pk>', CourseUpdateView.as_view(), name='edit-course'),
	path('courses/<int:pk>/add-lesson', LessonCreateView.as_view(), name='add-lesson'),
]