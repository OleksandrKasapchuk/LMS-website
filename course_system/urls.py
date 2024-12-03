from django.urls import path
from .views import *


urlpatterns = [
	path('', IndexView.as_view(), name='index'),

	path('courses/', CourseView.as_view(), name='course-list'),
	path('create-course', CourseCreateView.as_view(), name='add-course'),
	path('edit-course/<int:pk>', CourseUpdateView.as_view(), name='edit-course'),
	path('courses/<int:pk>', CourseDetailView.as_view(), name='course-details'),
	path('courses/<int:pk>/delete', CourseDeleteView.as_view(), name='course-delete'),

	path('courses/<int:pk>/add-lesson', LessonCreateView.as_view(), name='add-lesson'),
	path('courses/<int:course>/<int:pk>', LessonDetailView.as_view(), name='lesson-details'),
	path('courses/<int:course>/<int:pk>/delete', LessonUpdateView.as_view(), name='lesson-edit'),
	path('courses/<int:course>/<int:pk>/delete', LessonDeleteView.as_view(), name='lesson-delete'),
]