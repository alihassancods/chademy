from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Course(models.Model):
    title = models.CharField(max_length=120)
    dateCreated = models.DateField(auto_now_add=True)
    isPrivate = models.BooleanField(default=False)
    price = models.IntegerField(default=0)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name="createdCourses")
    accessibleBy = models.ManyToManyField(User,related_name="accessibleCourses",null=True)
    def __str__(self):
        return self.title    
class Lecture(models.Model):
    title = models.CharField(max_length=120)
    dateUploaded = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    viewCount = models.IntegerField(default=0)
    isPrivate = models.BooleanField(default=False)
    partOfCourse = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="lectures")
    videoFile = models.FileField(upload_to='videos/')
    transcriptionData = models.TextField(default=None)
    thumbnail = models.FileField(upload_to='thumbnails/',null=True)
    def __str__(self):
        return self.title