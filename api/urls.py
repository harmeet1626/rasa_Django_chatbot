# yourappname/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('index', index.as_view(), name='index'),
    path('chatbot', Chatbot.as_view(), name='chatbot'),
    path('documentUpload/',UploadDocumentTicket.as_view(), name='documentUpload'),
    path('user/chats/',ChatsListing.as_view(), name='user_chats'),
    
]
