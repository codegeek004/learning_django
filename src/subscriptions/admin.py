from django.contrib import admin
from .models import Subscription, UserSubscription, SubscriptionPrice

class SubscriptionPrice(admin.TabularInline):
	model = SubscriptionPrice
	readonly_fields = ['stripe_id']
	extra = 1


class SubscriptionAdmin(admin.ModelAdmin):
	inlines = [SubscriptionPrice]
	list_display = ['name', 'active']

admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(UserSubscription)
