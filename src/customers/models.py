from django.db import models
from django.conf import settings
import helpers.billing
from allauth.account.signals import (
	user_signed_up as allauth_user_signed_up,
	email_confirmed as allauth_email_confirmed
	)

User = settings.AUTH_USER_MODEL

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	stripe_id = models.CharField(max_length=120, null=True, blank=True)
	init_email = models.EmailField(blank=True, null=True)
	init_email_confirmed = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username

	# this will save the data in the database
	def save(self, *args, **kwargs):
		if not self.stripe_id:
			if self.init_email_confirmed and self.init_email:
				email = self.init_email
				if email != "" or email is not None:
					stripe_id = helpers.billing.create_customer(email=email,
						metadata={"user_id":self.user.id},
						raw=False)
					self.stripe_id = stripe_id
		# print(stripe_response)
		super().save(*args, **kwargs)
		# # post=save will not update
		# self.stripe_id = 'something else'
		#self.save()#recursively called too many times so it will cause an error

def allauth_user_signed_up_handler(request, user, *args, **kwargs):
	email = user.email 
	Customer.objects.create(
		user=user,
		init_email=email,
		init_email_confirmed=False,
		)

allauth_user_signed_up.connect(allauth_user_signed_up_handler)

def allauth_email_confirmed_handler(request, email_address, *args, **kwargs):
	qs = Customer.objects.filter(
		init_email=email_address,
		init_email_confirmed=False,
		)
	#does not send the save method or create the stripe customer
	# qs.update(init_email_confirmed=True)
	for obj in qs:
		obj.init_email_confirmed=True
		#send the signal
		obj.save()



allauth_email_confirmed.connect(allauth_email_confirmed_handler)





