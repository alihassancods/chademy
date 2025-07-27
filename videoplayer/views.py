from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponseForbidden
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from wsgiref.util import FileWrapper
import os

from . import models
from .forms import CourseForm, LectureForm

# Create your views here.


def allCourses(request):
    allCoursesInDatabase = models.Course.objects.all()
    context = {
        "courses": allCoursesInDatabase,
    }
    return render(request, "videoplayer/courses.html", context=context)


def viewCourse(request):
    courseID = request.GET.get("id")
    course = models.Course.objects.get(id=courseID)
    context = {
        "course": course,
    }
    return render(request, "videoplayer/viewCourse.html", context=context)


def watchLecture(request):
    if not request.user.is_authenticated:
        return redirect("google_login")
    lectureID = request.GET.get("id")
    lecture = models.Lecture.objects.get(id=lectureID)
    if not request.user in lecture.partOfCourse.accessibleBy.all():
        return HttpResponseForbidden("Get out of here. First buy the course and then come back here...")
    context = {
        "lecture": lecture
    }
    return render(request, "videoplayer/watchLecture.html", context=context)


@xframe_options_exempt
def stream_video(request, lecture_id):
    try:
        print(f"Streaming video for lecture_id: {lecture_id}")  # Debug print
        print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")  # Debug print
        lecture = models.Lecture.objects.get(id=lecture_id)
        path = lecture.videoFile.path
        print(f"Video path: {path}")  # Debug print
        print(f"Video name: {lecture.videoFile.name}")  # Debug print

        # Get the file size
        file_size = os.path.getsize(path)

        # Determine content type based on file extension
        content_type = 'video/webm' if path.lower().endswith('.webm') else 'video/mp4'

        # Handle range requests
        range_header = request.META.get('HTTP_RANGE', '').strip()
        range_re = range_header.replace('bytes=', '').split('-')
        range_start = int(range_re[0]) if range_re[0] else 0
        range_end = min(int(range_re[1]) if range_re[1] and range_re[1].isdigit(
        ) else file_size - 1, file_size - 1)

        # Open file in binary mode
        if not os.path.exists(path):
            print(f"File not found: {path}")  # Debug print
            return HttpResponseForbidden("Video file not found")

        file_obj = open(path, 'rb')

        if range_start > 0:
            file_obj.seek(range_start)

        content_length = range_end - range_start + 1

        response = FileResponse(
            FileWrapper(file_obj),
            content_type='video/mp4',  # Set to video/mp4 for now
            status=206 if range_header else 200,
        )

        # Set response headers
        response['Accept-Ranges'] = 'bytes'
        if range_header:
            response['Content-Range'] = f'bytes {range_start}-{range_end}/{file_size}'
        response['Content-Length'] = str(content_length)

        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['Content-Disposition'] = 'inline'
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'

        return response
    except models.Lecture.DoesNotExist:
        return HttpResponseForbidden("Access Denied")
    
# HACK : TRANSPORT THESE FUNCTIONS TO DASHBOARD INSTEAD OF BEING PLACED HERE
def createChooser(request):
    if not request.user.is_authenticated:
        return redirect("google_login")
    return render(request, "videoplayer/create.html")

def createCourse(request):
    if not request.user.is_authenticated:
        return redirect("google_login")
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.owner = request.user
            course.save()
            course.accessibleBy.add(request.user)
            course.save()
            return render(request, "videoplayer/createCourse.html", {"form": form, "success": True})
    else:
        form = CourseForm()
    return render(request, "videoplayer/createCourse.html", {"form": form})

def createLecture(request):
    if not request.user.is_authenticated:
        return redirect("google_login")
    if request.method == 'POST':
        form = LectureForm(request.POST, request.FILES)
        # Filter courses to only those owned by the current user
        form.fields['partOfCourse'].queryset = models.Course.objects.filter(owner=request.user)
        if form.is_valid():
            form.save()
            return render(request, "videoplayer/createLecture.html", {"form": form, "success": True})
    else:
        form = LectureForm()
        form.fields['partOfCourse'].queryset = models.Course.objects.filter(owner=request.user)
    return render(request, "videoplayer/createLecture.html", {"form": form})
