from django.db import models
from django.conf import settings
import helpers.billing
User = settings.AUTH_USER_MODEL

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	stripe_id = models.CharField(max_length=120, null=True, blank=True)

	def __str__(self):
		return self.user.username

	# this will save the data in the database
	def save(self, *args, **kwargs):
		if not self.stripe_id:
			email = self.user.email
			if email != "" or email is not None:
				stripe_id = helpers.billing.create_customer(email=email,raw=False)
				self.stripe_id = stripe_id
		# print(stripe_response)
		super().save(*args, **kwargs)
		# # post=save will not update
		# self.stripe_id = 'something else'
		#self.save()#recursively called too many times so it will cause an error
