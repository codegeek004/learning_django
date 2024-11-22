from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('<username>/', views.profile_view)
   ]