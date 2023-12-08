from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Chatroom(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now())

class Tickets(models.Model):
    ext_id = models.IntegerField()
    document_url = models.CharField(max_length=255, null=True, blank=True)
    chatroom = models.ForeignKey(Chatroom,on_delete=models.CASCADE,related_name="tickets")
    status = models.CharField(choices=(("Initiated","Initiated"),("In-Progress","In-Progress"),("Resolved","Resolved"),("Disposed","Disposed")),max_length=255)
    created_at = models.DateTimeField(default=datetime.now(),null=False)

class Chats(models.Model):
    chatroom = models.ForeignKey(Chatroom,on_delete=models.CASCADE,related_name="chats")
    question = models.CharField(max_length=255, null=False)
    response = models.CharField(max_length=255, null=True, blank=True)
    document_url = models.CharField(max_length=255, null=True, blank=True)
    ticket = models.ForeignKey(Tickets,on_delete=models.CASCADE,related_name="chats",null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now())




