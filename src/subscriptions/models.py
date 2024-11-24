from django.db import models
from django.contrib.auth.models import Group, Permission
from django.conf import settings
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL #auth.user

SUBSCRIPTION_PERMISSIONS = [
			('advanced', 'Advanced Perm'), #subscriptions advanced
			('pro', 'Pro Perm'), #subscriptions pro
			('basic', 'Basic Perm'), #subscriptions basic
			('basic_ai', 'Basic AI')
		]
ALLOW_CUSTOM_GROUPS = True

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


def user_sub_post_save(sender, instance, *args, **kwargs):
	user_sub_instance = instance
	user = user_sub_instance.user
	subscription_obj = user_sub_instance.subscription
	groups = subscription_obj.groups.all()
	if ALLOW_CUSTOM_GROUPS:
		user.groups.set(groups)
	else:
		subs_qs = Subscription.objects.filter(active=True).exclude(id=subscription_obj.id)
		subs_groups = subs_qs.values_list('groups__id', flat=True)
		subs_groups_set = set(subs_groups)
		groups_ids = groups.values.list('id', flat=True)
		current_groups = user.groups.all().values_list('id', flat=True)
		groups_ids_set = set(groups_ids)
		current_groups_set = set(current_groups) - subs_groups_set
		final_groups_ids = list(groups_ids_set | current_groups_set)
		user.groups.set(final_groups_ids)


post_save.connect(user_sub_post_save, sender=UserSubscription)







