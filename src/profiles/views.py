from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
User = get_user_model()


@login_required
def profile_list_view(request):
	context = {
		"object_list" : User.objects.filter(is_active=True)
	}
	return render(request, 'profiles/list.html', context)

# Create your views here.
@login_required
def profile_detail_view(request, username=None, *args, **kwargs):
	user = request.user 
	user_groups = user.groups.all()
	print(user_groups, 'user_groups')
	if user_groups.filter(name__icontains="basic").exists():
		return HttpResponse("Congrats")
	profile_user_obj = get_object_or_404(User, username=username)
	is_me = profile_user_obj == user
	context = {
		"object" : User.objects.filter(is_active=True),
		"instance": profile_user_obj,
		"owner": is_me,
	}
	
	return render(request, 'profiles/detail.html', context)
