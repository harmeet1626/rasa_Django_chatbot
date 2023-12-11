from rest_framework import serializers
from rasa_chat_app.models import Tickets,Chats

class UploadDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = ["ext_id","document"]

class ChatsListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chats
        fields = "__all__"

