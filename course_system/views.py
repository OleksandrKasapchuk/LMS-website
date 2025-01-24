from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import *
from django.views.generic import View, ListView, DetailView,UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from .forms import *
from .mixins import *


class CourseView(ListView):
	model = Course
	template_name = "course_system/course_list.html"
	context_object_name = "courses"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		category = self.request.GET.get('category', 'joined')
		
		if self.request.user.is_authenticated:
			if category == 'joined':
				# Отримуємо курси, на які підписаний користувач
				subscribed_courses = Subscription.objects.filter(user=self.request.user).values_list('course', flat=True)
				context['courses'] = Course.objects.filter(id__in=subscribed_courses)
			else:
				# Отримуємо курси, створені користувачем
				context['courses'] = Course.objects.filter(user=self.request.user)

			context['category'] = category

		return context


class CourseDetailView(DetailView):
	model = Course
	template_name = "course_system/course_info.html"
	context_object_name = "course"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['lessons'] = Lesson.objects.filter(course=Course.objects.get(pk=self.kwargs["pk"]))
		return context


class CourseCreateView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		return render(
			request,
			"course_system/add_course.html",
		)
	def post(self, request, *args, **kwargs):
		form = CourseCreateForm(request.POST, request.FILES)
		if form.is_valid():
			course = form.save(commit=False)
			course.user = self.request.user
			course.save()
			return redirect("index")
		else:
			pass


class CourseUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
	model = Course
	def get(self, request, pk, *args, **kwargs):
		return render(
			request,
			"course_system/edit_course.html",
			context={"course": Course.objects.get(pk=pk)}
		)
	def post(self, request, pk, *args, **kwargs):
		course = Course.objects.get(pk=pk)
		course.name = request.POST.get('name')
		if request.FILES.get('cover') != None:
			course.cover = request.FILES.get('cover')
		course.save()
		return redirect(f"/{course.pk}")


class LessonCreateView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		course = Course.objects.get(pk=self.kwargs['pk'])
		if course.user == request.user:
			return render(
				request,
				"course_system/add_lesson.html",
			)
		else:
			raise PermissionDenied

	def post(self, request, *args, **kwargs):
		form = LessonCreateForm(request.POST, request.FILES)
		if form.is_valid():
			lesson = form.save(commit=False)
			course = get_object_or_404(Course, id=self.kwargs['pk'])
			lesson.course = course
			if course.user == request.user:
				lesson.save()
				return redirect("course-details", pk=lesson.course.pk)
			else:
				raise PermissionDenied
		else:
			pass


class LessonDetailView(LoginRequiredMixin,DetailView):
	model = Lesson
	template_name = "course_system/lesson_info.html"
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		lesson = self.get_object()
		user = self.request.user
		answer = Answer.objects.filter(user=user, lesson=lesson).first()
		tab_name = self.request.GET.get('tab', 'about')

		if tab_name == 'about':
			context['lesson'] = lesson
		elif tab_name == 'answers':
			if user == lesson.course.user:
				context["answers"] = Answer.objects.filter(lesson=self.object, user_send=True)
			else:
				raise PermissionDenied
		if answer:
			context["user_send"] = answer.user_send
			context['answer'] = answer

		context["tab"] = tab_name

		# Перевіряємо, чи користувач здав роботу
		user_answer = lesson.answers.filter(user=user).first()
		context['user_has_answered'] = user_answer is not None

		if user_answer:
			# Додаємо відповідь користувача
			context['user_answer'] = user_answer

			# Додаємо оцінку за відповідь, якщо вона є
			context['mark'] = user_answer.mark

		return context


class CourseDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
	model = Course
	template_name = "course_system/delete.html"
	context_object_name = "object"

	def get_success_url(self) -> str:
		return reverse_lazy("index")


class LessonDeleteView(LoginRequiredMixin,LessonUserIsOwnerMixin, DeleteView):
	model = Lesson
	template_name = "course_system/delete.html"
	context_object_name = "object"

	def get_success_url(self) -> str:
		return reverse_lazy("course-details", kwargs={"pk": self.kwargs['course']})


class LessonUpdateView(LoginRequiredMixin, LessonUserIsOwnerMixin, UpdateView):
	model = Lesson
	def get(self, request, pk, *args, **kwargs):
		return render(
			request,
			"course_system/edit_lesson.html",
			context={"lesson": Lesson.objects.get(pk=pk)}
		)
	def post(self, request, pk, *args, **kwargs):
		lesson = Lesson.objects.get(pk=pk)
		lesson.name = request.POST.get('name')
		lesson.content = request.POST.get('content')

		if request.POST.get('date_to'):
			lesson.date_to = request.POST.get('date_to')

		if request.FILES.get('upload_data') != None:
			lesson.upload_data = request.FILES.get('upload_data')
		lesson.save()
		return redirect(f"/{lesson.course.pk}/{pk}")


class SubscriptionView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		return render(
			request,
			"course_system/subscription.html"
		)
	
	def post(self, request, *args, **kwargs):
		code = request.POST.get("code")
		course = get_object_or_404(Course, code=code)  

		if not request.user == course.user:
			if not Subscription.objects.filter(user=request.user, course=course).exists():
				
				Subscription.objects.create(user=request.user, course=course)
				return redirect("index")  # Перенаправляємо на список підписок

		return redirect("course_detail", pk=course.pk)
	

def send_answer(request, course,pk):
	answer, created = Answer.objects.get_or_create(user=request.user, lesson=Lesson.objects.get(pk=pk))
	if answer != None:
		answer.user_send = True
		answer.save()
	else:
		created.user_send = True
		created.save()
	return redirect(f"/{course}/{pk}")

import logging

logger = logging.getLogger(__name__)

class UploadAnswerFileView(View):
    def post(self, request, course_pk, lesson_pk, *args, **kwargs):
        try:
            files = request.FILES.getlist('files[]')
            if not files:
                return JsonResponse({'success': False, 'error': 'No files received'}, status=400)

            logger.info(f"Received files: {files}")
            
            # Отримуємо або створюємо відповідь
            answer, created = Answer.objects.get_or_create(
                user=request.user,
                lesson=Lesson.objects.get(pk=lesson_pk),
            )
            if answer.user_send:
                return JsonResponse({'success': False, 'error': "Return your answer before uploading new files."}, status=500)
            uploaded_files = []

            # Завантажуємо кожен файл
            for file in files:
                logger.info(f"Processing file: {file.name}")
                if answer != None:
                    uploaded_file = UploadedFile.objects.create(answer=answer, file=file)
                else:
                    uploaded_file = UploadedFile.objects.create(answer=created, file=file)

                uploaded_files.append({
                    'id': uploaded_file.pk,
                    'url': uploaded_file.file.url,
                    'name': uploaded_file.file.name.split('/')[-1],
                    'preview': (
                        f'<img src="{uploaded_file.file.url}" style="width: 90px; height: 60px;">'
                        if file.content_type.startswith('image') 
                        else '<span class="material-symbols-outlined" style="font-size: 48px;">insert_drive_file</span>'
                    ),
                })

            logger.info(f"Successfully uploaded files: {uploaded_files}")
            return JsonResponse({'success': True, 'files': uploaded_files})

        except Exception as e:
            logger.error(f"Error while uploading files: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


class AnswerReturnView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        lesson = get_object_or_404(Lesson, pk=self.kwargs['pk'])
        user = request.user

        # Отримуємо відповідь користувача
        answer = lesson.answers.filter(user=user).first()

        if answer:
            answer.user_send = False
            answer.save()
            return redirect(f'/{lesson.course.pk}/{lesson.pk}')
        else:
            return JsonResponse({'success': False, 'message': 'Робота не знайдена.'}, status=404)


class DeleteUploadedFileView(LoginRequiredMixin, View):
	def post(self, request, *args, **kwargs):
		file = get_object_or_404(UploadedFile, pk=self.kwargs["pk"])
		lesson = file.answer.lesson

		file.delete()

		return redirect(f'/{lesson.course.pk}/{lesson.pk}')


class MarkView(LoginRequiredMixin, View):
	def post(self, request, *args, **kwargs):
		answer = get_object_or_404(Answer, pk=self.kwargs["pk"])
		
		mark = request.POST.get('mark')
		answer.mark = mark
		answer.save()

		return redirect(f"/{answer.lesson.course.pk}/{answer.lesson.pk}?tab=answers")

def cancel_subscription(request, pk):
	course = get_object_or_404(Course, pk=pk)
	sub = get_object_or_404(Subscription, course=course,user=request.user)
	sub.delete()
	return redirect("index")


class CommentDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        if comment.user == request.user:
            comment.delete()
            return JsonResponse({'success': True})
        else:
            raise PermissionDenied


class CommentCreateView(LoginRequiredMixin, View):
	def post(self, request,pk, *args, **kwargs):
		lesson = get_object_or_404(Lesson, pk=pk)
		content = request.POST.get('content')
		try:
			comment = Comment.objects.create(
			lesson=lesson,
			user=request.user,
			content=content
			)
			if request.headers.get('x-requested-with') == 'XMLHttpRequest':
				return JsonResponse({
					'success': True,
					'username': request.user.username,
					'content': comment.content,
					'user_url': reverse_lazy('user-info', kwargs={"pk":comment.user.pk}),
					"comment": comment.pk
				})
			return redirect('lesson-details', pk=comment.lesson.pk, course=comment.lesson.course.pk)
		except Exception as e:
			if request.headers.get('x-requested-with') == 'XMLHttpRequest':
				return JsonResponse({'success': False, 'error': f'Error creating comment: {str(e)}'})