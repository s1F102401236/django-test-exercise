from django.urls import path
from . import views

app_name = 'todo'  # これが名前空間の宣言

urlpatterns = [
    path('', views.index, name='index'),
    # 他のパス
]