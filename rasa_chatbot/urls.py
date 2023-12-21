# yourprojectname/urls.py
from django.contrib import admin
from django.urls import include, path
from api.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
]
