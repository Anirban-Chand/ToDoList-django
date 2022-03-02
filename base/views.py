from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task


class CustomLoginView(LoginView):
    template_name = 'base\login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


# ListView looks for a template with name -> <model_name>_list
class TaskList(LoginRequiredMixin, ListView):
    model = Task

    # ListView in Django by default looks for 'object_list' variable to iterate through
    # to change the varible name from 'object_list' to other name, we add the line below
    context_object_name = 'tasks'

    # this method provides sand-boxing among all the users. so that a user can access it's own data only and not other's
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user = self.request.user)
        context["count"] = context["tasks"].filter(complete=False).count()
        return context
    


# DetailView looks for a template with name -> <model_name>_detail
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    # previously when we wanted to create a task we had to choose a user from list of all users.
    # To prevent this and add task under only the logged in user we are adding this below method
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


# by default UpdateView also looks for '<model_name>_form.html' template
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')