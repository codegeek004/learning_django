from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/', views.profile_view),
    path('', views.profile_list_view),
   ]