from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView

from .models import task


# Create your views here.

def home(request):
    return render(request,'home.html')

class CustomLoginView(LoginView):
    template_name = 'login.html'
    field = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('Task')


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('Task')
        return super(RegisterView, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = task
    context_object_name = 'Task'
    template_name = 'list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Task'] = context['Task'].filter(user=self.request.user)
        context['count'] = context['Task'].filter(completed=False).count()

        return context


class TaskCreate(LoginRequiredMixin, CreateView):
    model = task
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('task-create')
    template_name = 'taskcreate.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = task
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('Task')
    template_name = 'taskcreate.html'


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = task
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('Task')
    template_name = 'taskdelete.html'


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = task
    template_name = 'taskdetail.html'
