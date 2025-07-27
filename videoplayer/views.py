from django.shortcuts import render, redirect,get_object_or_404
from django.http import FileResponse, HttpResponseForbidden
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.conf import settings
from wsgiref.util import FileWrapper
from transcriptor.views import transcribe
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
    
    lecture = get_object_or_404(models.Lecture, id=request.GET.get("id"))
    course = lecture.partOfCourse

    if request.user not in list(course.accessibleBy.all()):
        return redirect(
            "buy-course",
            course_uuid=course.uuid,
        )
    

    return render(request, "videoplayer/watchLecture.html", {"lecture": lecture})


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
            from chat.models import Group
            group = Group.objects.create(name=course.uuid)
            
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
        import threading
        if form.is_valid():
            lecture = form.save()
            # return render(request, "videoplayer/createLecture.html", {"form": form, "success": True})
            def _transcribe():
                video_path = lecture.videoFile.path
                audio_path = os.path.join(
                    settings.MEDIA_ROOT,
                    "lectures/audio",
                    f"{os.path.splitext(os.path.basename(video_path))[0]}.mp3",
                )
                os.makedirs(os.path.dirname(audio_path), exist_ok=True)

                text = transcribe(video_path, audio_path)
                lecture.transcriptionData = text
                lecture.save(update_fields=["transcriptionData"])

            threading.Thread(target=_transcribe, daemon=True).start()
            return redirect("main:dashboard")
    else:
        form = LectureForm()
        form.fields['partOfCourse'].queryset = models.Course.objects.filter(owner=request.user)
    return render(request, "videoplayer/createLecture.html", {"form": form})
