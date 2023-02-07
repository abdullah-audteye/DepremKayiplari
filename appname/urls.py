from django.urls import path
from . import views

urlpatterns = [
    path('user/create/', views.user_create, name='user_create'),
    path('user/list/', views.user_list, name='user_list'),
]