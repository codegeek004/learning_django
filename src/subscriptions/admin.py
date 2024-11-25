from django.contrib import admin
from .models import Subscription, UserSubscription, SubscriptionPrice

class SubscriptionPrice(admin.TabularInline):
	model = SubscriptionPrice
	extra = 0


class SubscriptionAdmin(admin.ModelAdmin):
	inlines = [SubscriptionPrice]
	list_display = ['name', 'active', 'stripe_id']

admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(UserSubscription)
