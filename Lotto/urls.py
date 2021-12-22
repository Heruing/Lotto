from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('recommend/', include('recommend.urls')),
    path('detail/<int:num>', include('recommend.urls')),
]
