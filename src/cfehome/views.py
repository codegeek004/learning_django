import pathlib
from pathlib import Path
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from visits.models import PageVisit
from django.conf import settings


#if no admin is found for the staff required
LOGIN_URL = settings.LOGIN_URL

this_dir = pathlib.Path(__file__).resolve().parent

def home_page_view(request, *args, **kwargs):
	return about_view(request, *args, **kwargs)


def about_view(request, *args, **kwargs):
	qs = PageVisit.objects.all()
	page_qs = PageVisit.objects.filter(path=request.path)
	try:
		percent = (page_qs.count() * 100.0) / qs.count()
	except:
		percent = 0
	my_title = "My Page"
	html_template = "home.html"
	my_context = {
		"page_title": my_title,
		"page_visit_count": page_qs.count(),
		"total_page_visit_count": qs.count(),
		"percent": percent
	}
	PageVisit.objects.create(path=request.path)
	return render(request, html_template, my_context)




def my_old_home_page(request, *args, **kwargs):
	my_title = "My page"
	my_context = {
		"page_title" : my_title
	}
	html_ = """
		<!DOCTYPE html>
		<html>
		<body>
			<h1>{page_title}</h1>
		</body>
		</html>
		""".format(**my_context) #page_title=my_title
		# html_file_path = this_dir / "home.html"
		# html_ = html_file_path.read_text()
	return HttpResponse(html_)

VALID_CODE = 'abc123'
def pw_protected_view(request, *args, **kwargs):
	is_allowed = request.session.get('protected_page_allowed') or 0
	print(request.session.get('protected_page_allowed'), type(request.session.get('protected_page_allowed') ))
	if request.method == 'POST':
		user_pw_sent = request.POST.get('code') or None
		print(user_pw_sent, 'user pw sent')	 
		if user_pw_sent == VALID_CODE:
			request.session['protected_page_allowed'] = 1
	
	if is_allowed:
		return render(request, 'protected/view.html')
	return render(request, "protected/entry.html")



@login_required
def user_only_view(request, *args, **kwargs):
	return render(request, 'protected/user_only_view.html')




@staff_member_required(login_url=LOGIN_URL)
def staff_only_view(request, *args, **kwargs):
	return render(request, 'protected/user_only_view.html')






