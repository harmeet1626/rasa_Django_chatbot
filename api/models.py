from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from api.utils import generate  




class Chatroom(models.Model):
    class Meta:
        db_table = "Chatroom"
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)


class Chats(models.Model):
    class Meta:
        db_table = "Chats"
    chatroom = models.ForeignKey(Chatroom,on_delete=models.PROTECT,related_name="chats")
    question = models.CharField(max_length=255, null=True, blank=True)
    response = models.CharField(max_length=255, null=True, blank=True)
    document = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(choices=(("text","text"),("file","file")),default="text",max_length=255)
    created_at = models.DateTimeField(auto_now_add=True,)


class Tickets(models.Model):
    class Meta:
        db_table = "Tickets"
    ext_id = models.CharField(max_length=255,null=False, blank=False, unique = True)
    text =models.CharField(max_length=255,null=False, blank=False)
    document = models.FileField(upload_to =  "static/documents", null = True ,blank = True )
    chat= models.OneToOneField(Chats, on_delete=models.PROTECT, related_name="tickets")
    status = models.CharField(choices=(("Initiated","Initiated"),("In-Progress","In-Progress"),("Resolved","Resolved"),("Disposed","Disposed")),max_length=255)
    created_at = models.DateTimeField(auto_now_add=True,null=False)



class Restaurants(models.Model):
    class Meta:
        db_table = "restaurants"
    name = models.CharField(max_length=120,null=False, blank=False, unique = True)

class Bookings(models.Model):
    class Meta:
        db_table = "bookings"
    ext_id = models.CharField(max_length=20,null=False, blank=False, unique = True)
    user = models.ForeignKey(Restaurants,on_delete=models.PROTECT)
    restaurant = models.ForeignKey(User,on_delete=models.PROTECT, null=False, blank=False,)
    cuisine =models.CharField(max_length=255,null=False, blank=False)
    people_num = models.IntegerField()
    outdoor_seating= models.BooleanField(default=False)
    booking_date = models.DateTimeField(null=False)
    created_at = models.DateTimeField(auto_now_add=True,null=False)


    def check_unique(self, ext_id):
        return not Bookings.objects.filter(ext_id=ext_id).exists()
    
    def save(self, *args, **kwargs):
        if not self.ext_id:
            self.ext_id = "BKNG-"+generate.generate_unique_ext(
                self, 6)
        super(Bookings, self).save(*args, **kwargs)
