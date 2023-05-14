from django.urls import path
from .views import TaskView, TasksView, SubTaskView

app_name = 'task'

urlpatterns = [
    path('', TasksView.as_view()),
    path('/<int:pk>', TaskView.as_view(), name='TaskView'),
    path('/sub/<int:pk>', SubTaskView.as_view(), name='SubTaskView'),
]