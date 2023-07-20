from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import TaskList, TaskCreate, TaskUpdate, TaskDelete, TaskDetailView, RegisterView, CustomLoginView, home

urlpatterns = [
    path('',home,name='home'),
    path('login/',CustomLoginView.as_view(),name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register/',RegisterView .as_view(), name='register'),
    path('Task/',TaskList.as_view(),name='Task'),
    path('create/', TaskCreate.as_view(), name='task-create'),
    path('update/<int:pk>',TaskUpdate.as_view(),name='task-update'),
    path('delete/<int:pk>', TaskDelete.as_view(), name='task-delete'),
    path('details/<int:pk>', TaskDetailView.as_view(), name='task-details')

]
