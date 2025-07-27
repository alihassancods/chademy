from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name


class PrivateMessage(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_private')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_private')
    text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sent_at']


class GroupMessage(models.Model):
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sent_at']
