from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.index, name='index'),
    path('task/<int:pk>/like/', views.add_like, name='add_like'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
]