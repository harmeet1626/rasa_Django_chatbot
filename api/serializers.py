from rest_framework import serializers
from api.models import Tickets,Chats

class UploadDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = ["document",]

class ChatsListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chats
        exclude = ("chatroom",)

