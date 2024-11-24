from django.core.management.base import BaseCommand
from subscriptions.models import Subscription


class Command(BaseCommand):
	def handle(self, *args: any, **options: any):
		# print("Hello World")
		qs = Subscription.objects.filter(active=True)
		for obj in qs:
			# print(obj.groups.all())
			sub_perms = obj.permissions.all() 
			for group in obj.groups.all():
				print('group wale for loop mai')
				print(group)
				for per in obj.permissions.all():
					print('per wale for loop mai')
					print(per)
					group.permissions.set(sub_perms)
			# print(obj.permissions.all())