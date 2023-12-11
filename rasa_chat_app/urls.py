# yourappname/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('chatbot', Chatbot.as_view(), name='chatbot'),
    path('documentUpload/',UploadDocumentTicket.as_view(), name='documentUpload')
    
]
