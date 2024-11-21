from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model


def login_view(request):
	print(request.method, request.POST or None)
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		if all([username,password]):
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				print('login here!')
				return redirect('/')
	return render(request, 'auth/login.html',{})




#########Not a good way to register. We will use allauth#############
#this way also we can create register
User = get_user_model()

def register_view(request):
	if request.method == "POST":
		username = request.POST.get('username')
		email = request.POST.get('email')
		try:
			User.objects.create_user(username, email=None, password=None)
		except:
			pass
	return render(request, 'auth/register.html')