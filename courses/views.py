from django.shortcuts import render
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin


from courses.models import Course


# Create your views here.


class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)

class OwnerEditMixin:
    def form_valid(self,form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class OwnerCourseMixin(OwnerMixin,LoginRequiredMixin,PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')

class OwnCourseEditMixin(OwnerCourseMixin,OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'
class ManageCourseListView(OwnerCourseMixin,ListView):
    model = Course
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'

class CourseCreateView(OwnCourseEditMixin,CreateView):
    permission_required = 'courses.add_course'

class CourseUpdateView(OwnCourseEditMixin,UpdateView):
    permission_required = 'courses.change_course'

class CourseDeleteView(OwnCourseEditMixin,DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


