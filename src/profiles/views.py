from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
User = get_user_model()

# Create your views here.
@login_required
def profile_view(request, username=None, *args, **kwargs):
	user = request.user 
	profile_user_obj = get_object_or_404(User, username=username)
	return HttpResponse(f"Hello there! {username} - {profile_user_obj.id}")