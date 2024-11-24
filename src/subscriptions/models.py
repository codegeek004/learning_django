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
	groups_ids = []
	if subscription_obj is not None:
		groups = subscription_obj.groups.all()
		groups_ids = groups.values_list('id', flat=True)
	groups = subscription_obj.groups.all()
	# user.groups.set(groups)	
	# this will be useful when you want to add a group which is not a part of the subscription model but still
	# you want to add without losing the integrity then you can use the ALLOW_CUSTOM_GROUPS approach
	if not ALLOW_CUSTOM_GROUPS:
		user.groups.set(groups_ids)
	else:
		subs_qs = Subscription.objects.filter(active=True)
		if subscription_obj is not None:
			subs_qs = subs_qs.exclude(id=subscription_obj.id)
		subs_groups = subs_qs.values_list('groups__id', flat=True)
		subs_groups_set = set(subs_groups)
		# groups_ids = groups.values.list('id', flat=True)
		current_groups = user.groups.all().values_list('id', flat=True)
		groups_ids_set = set(groups_ids)
		current_groups_set = set(current_groups) - subs_groups_set
		final_groups_ids = list(groups_ids_set | current_groups_set)
		user.groups.set(final_groups_ids)
# Exclude Groups of Other Subscriptions:
# The function fetches all groups from active subscriptions except the current one.
# These are stored in subs_groups_set.
# Calculate Current Groups:
# The user's current groups are fetched and converted into a set, current_groups_set.
# Remove Overlapping Groups:
# Any groups linked to other active subscriptions (subs_groups_set) are removed from current_groups_set.
# Combine Groups:
# Groups linked to the current subscription (groups_ids_set) are combined with the remaining groups in current_groups_set.
# Update User Groups:
# The user’s groups are updated with the resulting list, final_groups_ids.



post_save.connect(user_sub_post_save, sender=UserSubscription)







