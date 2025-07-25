from django.db import models

# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=120)
    dateCreated = models.DateField(auto_now_add=True)
    isPrivate = models.BooleanField(default=False)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.title    
class Lecture(models.Model):
    title = models.CharField(max_length=120)
    dateUploaded = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    viewCount = models.IntegerField()
    isPrivate = models.BooleanField(default=False)
    partOfCourse = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="lectures")
    videoFile = models.FileField(upload_to='videos/')

    def __str__(self):
        return self.title