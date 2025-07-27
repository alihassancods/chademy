# chat/urls.py   (HTTP routes for templates)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.group_list, name='group_list'),
    path('inbox/<str:username>/', views.private_chat, name='private_chat'),
    path('<uuid:group_name>/', views.group_chat, name='group_chat'),
]
