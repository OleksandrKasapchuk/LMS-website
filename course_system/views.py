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
	template_name = "course_system/course-list.html"
	context_object_name = "courses"


class CourseDetailView(DetailView):
	model = Course
	template_name = "course_system/course-info.html"
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
		return render(
			request,
			"course_system/add_lesson.html",
		)
	def post(self, request, *args, **kwargs):
		form = LessonCreateForm(request.POST, request.FILES)
		if form.is_valid():
			lesson = form.save(commit=False)
			lesson.course = get_object_or_404(Course, id=self.kwargs['pk'])
			lesson.save()
			return redirect("course-info", pk=lesson.course.pk)
		else:
			pass
