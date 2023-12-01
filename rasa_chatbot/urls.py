# yourprojectname/urls.py
from django.contrib import admin
from django.urls import include, path
from rasa_chat_app.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('yourappname/', include('rasa_chat_app.urls')),
    path('', index )
]
