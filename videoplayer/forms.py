
from django import forms
from .models import Course, Lecture

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'isPrivate', 'price']

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['title', 'description', 'isPrivate', 'partOfCourse', 'videoFile']
