from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import *
from django.views.generic import View, ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .forms import *
from .mixins import *


class IndexView(TemplateView):
	template_name = "course_system/index.html"


class CourseView(ListView):
	model = Course
	template_name = "course_system/course_list.html"
	context_object_name = "courses"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		category = self.request.GET.get('category', 'joined')

		if category == 'joined' and self.request.user.is_authenticated:
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
			return redirect("course-list")
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
		return redirect(f"/courses/{course.pk}")


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


class LessonDetailView(DetailView):
	model = Lesson
	template_name = "course_system/lesson_info.html"
	context_object_name = "lesson"

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
					'avatar_url': request.user.avatar.url,
					'date_published': comment.date_published,
					'user_url': reverse_lazy('user-info', kwargs={"pk":comment.user.pk}),
				})
			return redirect('lesson-details', pk=comment.lesson.pk, course=comment.lesson.course.pk)
		except Exception as e:
			if request.headers.get('x-requested-with') == 'XMLHttpRequest':
				return JsonResponse({'success': False, 'error': str(e)})

class CourseDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
	model = Course
	template_name = "course_system/delete.html"
	context_object_name = "object"

	def get_success_url(self) -> str:
		return reverse_lazy("course-list")


class LessonDeleteView(LoginRequiredMixin,LessonUserIsOwnerMixin, DeleteView):
	model = Lesson
	template_name = "course_system/delete.html"
	context_object_name = "object"

	def get_success_url(self) -> str:
		return reverse_lazy("course-details", kwargs={"pk": self.kwargs['course']})


class LessonUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
	model = Course
	def get(self, request, pk, *args, **kwargs):
		return render(
			request,
			"course_system/edit_lesson.html",
			context={"lesson": Lesson.objects.get(pk=pk)}
		)
	def post(self, request, pk, *args, **kwargs):
		lesson = Lesson.objects.get(pk=pk)
		lesson.name = request.POST.get('name')
		if request.FILES.get('upload_data') != None:
			lesson.upload_data = request.FILES.get('upload_data')
		lesson.save()
		return redirect(f"/courses/{lesson.course.pk}/{pk}")


class SubscriptionView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		return render(
			request,
			"course_system/subscription.html"
		)
	
	def post(self, request, *args, **kwargs):
		code = request.POST.get("code")  # Отримуємо ID курсу з параметрів URL
		course = get_object_or_404(Course, code=code)  # Знаходимо курс або повертаємо 404

		# Перевіряємо, чи користувач вже підписаний на курс
		if not Subscription.objects.filter(user=request.user, course=course).exists():
			# Створюємо нову підписку
			Subscription.objects.create(user=request.user, course=course)
			return redirect("course-list")  # Перенаправляємо на список підписок

		# Якщо вже підписаний, перенаправляємо назад
		return redirect("course_detail", pk=course.pk)