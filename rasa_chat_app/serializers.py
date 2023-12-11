from rest_framework import serializers
from rasa_chat_app.models import Tickets

class UploadDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = ["ext_id","document"]
