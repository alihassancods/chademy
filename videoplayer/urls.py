"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

app_name = "videoplayer"

urlpatterns = [
    path('', views.allCourses, name='all_courses'),
    path('course', views.viewCourse, name='view_course'),
    path('lecture', views.watchLecture, name='watch_lecture'),
    path('stream/<int:lecture_id>/', views.stream_video, name='stream_video'),
    path("courses/",views.allCourses,name="allCourses"),
    path("course/",views.viewCourse,name="viewCourse"),
    path("lecture/",views.watchLecture,name="watchLecture"),
path("create/", views.createChooser, name="create"),
path("create/course", views.createCourse, name="createCourse"),
path("create/lecture", views.createLecture, name="createLecture"),

]
