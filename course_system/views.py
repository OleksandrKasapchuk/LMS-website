from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import *
from django.views.generic import View, ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .forms import *


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
			course.owner = self.request.user
			course.save()
			return redirect("course-list")
		else:
			pass