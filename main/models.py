from django.db import models
from django.contrib.auth.models import User
from django.db import models
# Create your models here.
class UserProfile(models.Model):
    CATEGORY_CHOICES = (
    ("student", "Student"),
    ("teacher", "Teacher"),
    )
    user   = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    def __str__(self):
        return f"{self.user.username} ({self.category})"