from django.urls import path
from . import views

app_name = 'recommend'

urlpatterns = [
    path('<int:page>/', views.index, name='index'),
    path('detail/<int:num>', views.detail, name='detail'),
]
