from django.shortcuts import render,HttpResponse

# Create your views here.
def allCourses(request):
    return HttpResponse("All Courses page")

def viewCourse(request):
    return HttpResponse("View the Course page")

def watchLecture(request):
    return HttpResponse("Watch any lecture of a course")