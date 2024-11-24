from django.db import models
from django.contrib.auth.models import Group, Permission
from django.conf import settings

User = settings.AUTH_USER_MODEL #auth.user

SUBSCRIPTION_PERMISSIONS = [
			('advanced', 'Advanced Perm'), #subscriptions advanced
			('pro', 'Pro Perm'), #subscriptions pro
			('basic', 'Basic Perm'), #subscriptions basic
			('basic_ai', 'Basic AI')
		]

class Subscription(models.Model):
	name = models.CharField(max_length=120)
	active = models.BooleanField(default=True)
	groups = models.ManyToManyField(Group)
	permissions = models.ManyToManyField(
		Permission,
		limit_choices_to = {
		'content_type__app_label':'subscriptions', 
		# 'codename__icontains':'basic',
		'codename__in':[ X[0] for X in SUBSCRIPTION_PERMISSIONS]
		}
	)
	class Meta:
		permissions = SUBSCRIPTION_PERMISSIONS
	def __str__(self):
		return self.name

class UserSubscription(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
	active = models.BooleanField(default=True)

	def __str__(self):
		return f"{self.user}"