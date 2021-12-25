from django.contrib import admin
from django.urls import path, include
from ..recommend.views import index


urlpatterns = [
    path('/', index),
    path('admin/', admin.site.urls),
    path('recommend/', include('recommend.urls')),
    path('detail/<int:num>', include('recommend.urls')),
]
