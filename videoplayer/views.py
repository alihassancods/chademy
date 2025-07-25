from django.shortcuts import render,HttpResponse
from . import models
# Create your views here.
def allCourses(request):
    allCoursesInDatabase = models.Course.objects.all()
    context = {
        "courses":allCoursesInDatabase,
    }
    return render(request,"videoplayer/courses.html",context=context)

def viewCourse(request):
    courseID = request.GET.get("id")
    course = models.Course.objects.get(id=courseID)
    context = {
        "course": course,
    }
    return render(request,"videoplayer/viewCourse.html",context=context)

def watchLecture(request):
    lectureID = request.GET.get("id")
    lecture = models.Lecture.objects.get(id=lectureID)
    context = {
        "lecture":lecture
    }
    return render(request,"videoplayer/watchLecture.html",context=context)