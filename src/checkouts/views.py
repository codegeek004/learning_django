from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from subscriptions.models import SubscriptionPrice
from django.contrib import messages
from django.conf import settings
BASE_URL = settings.BASE_URL
# Create your views here.
def product_price_redirect_view(request, price_id=None, *args, **kwargs):
	request.session['checkout_subscription_price_id'] = price_id
	return redirect('stripe-checkout-start')
    

def checkout_view(request, price_id, *args, **kwargs):
	course_id = checkout_subscription_price_id
	print(course_id)
	if not course_id:
		messages.success('Unable to fetch your price details. Please try again later')
		return redirect('/pricing')
	username = request.user 
	print(username,'username')
	return render(request, 'checkout/receipt.html', )














