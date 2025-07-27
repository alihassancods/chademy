from django.db import models

# Create your models here.
# payments/models.py

class Course(models.Model):
    title = models.CharField(max_length=200)
    stripe_price_id = models.CharField(max_length=120)   # price_...
    content = models.TextField()

class PaymentHistory(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    email = models.EmailField()
    stripe_session_id = models.CharField(max_length=250)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)