from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Message(models.Model):
    text = models.CharField(max_length=500)
    sender = models.ForeignKey(User , on_delete=models.CASCADE,related_name='sender')
    receiver = models.ForeignKey(User , on_delete=models.CASCADE,related_name='receiver')
    created = models.DateTimeField(auto_now_add=True)
