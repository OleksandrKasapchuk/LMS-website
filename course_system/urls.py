from django.urls import path
from .views import *


urlpatterns = [
	path('', CourseView.as_view(), name='index'),
    
	path('join', SubscriptionView.as_view(), name='join-course'),
	path('create-course', CourseCreateView.as_view(), name='add-course'),
    path("cancel-subscription/<int:pk>", cancel_subscription, name="cancel-subscription"),
    
	path('<int:pk>', CourseDetailView.as_view(), name='course-details'),
    
	path('edit-course/<int:pk>', CourseUpdateView.as_view(), name='edit-course'),
	path('delete-course/<int:pk>', CourseDeleteView.as_view(), name='course-delete'),

	path('<int:pk>/add-lesson', LessonCreateView.as_view(), name='add-lesson'),
    
	path('<int:course>/<int:pk>', LessonDetailView.as_view(), name='lesson-details'),
    
	path('<int:course>/<int:pk>/edit', LessonUpdateView.as_view(), name='lesson-edit'),
	path('<int:course>/<int:pk>/delete', LessonDeleteView.as_view(), name='lesson-delete'),
    
	path('<int:course>/<int:pk>/comment-create', CommentCreateView.as_view(), name='add-comment'),
	path('delete-comment/<int:pk>', CommentDeleteView.as_view(), name='delete-comment'),


	path('lesson-answer-upload/<int:course_pk>/<int:lesson_pk>/', UploadAnswerFileView.as_view(), name='lesson-answer-upload'),
    path("<int:course>/<int:pk>/send-answer", send_answer, name='send-answer'),
	path('<int:course>/<int:pk>/return-answer', AnswerReturnView.as_view(), name='return-answer'),
    
	path('delete-file/<int:pk>', DeleteUploadedFileView.as_view(), name='delete-file'),
	path('mark/<int:pk>', MarkView.as_view(), name='mark-answer'),
]