from django.db import models
from videoplayer.models import Course
# Create your models here.
# payments/models.py


class PaymentHistory(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    email = models.EmailField()
    stripe_session_id = models.CharField(max_length=250)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)