from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Chatroom(models.Model):
    class Meta:
        db_table = "Chatroom"
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now())


class Chats(models.Model):
    class Meta:
        db_table = "Chats"
    chatroom = models.ForeignKey(Chatroom,on_delete=models.CASCADE,related_name="chats")
    question = models.CharField(max_length=255, null=True, blank=True)
    response = models.CharField(max_length=255, null=True, blank=True)
    document = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(choices=(("text","text"),("file","file")),default="text",max_length=255)
    created_at = models.DateTimeField(default=datetime.now())


class Tickets(models.Model):
    class Meta:
        db_table = "Tickets"
    ext_id = models.CharField(max_length=255,null=False, blank=False, unique = True)
    text =models.CharField(max_length=255,null=False, blank=False)
    document = models.FileField(upload_to =  "static/documents", null = True ,blank = True )
    chat= models.OneToOneField(Chats, on_delete=models.CASCADE, related_name="tickets")
    status = models.CharField(choices=(("Initiated","Initiated"),("In-Progress","In-Progress"),("Resolved","Resolved"),("Disposed","Disposed")),max_length=255)
    created_at = models.DateTimeField(default=datetime.now(),null=False)



