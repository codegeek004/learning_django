# Generated by Django 5.0.9 on 2024-11-25 12:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0010_subscription_stripe_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_id', models.CharField(blank=True, max_length=120, null=True)),
                ('interval', models.CharField(choices=[('month', 'Monthly'), ('year', 'Yearly')], default='month', max_length=120)),
                ('price', models.DecimalField(decimal_places=2, default=99.99, max_digits=10)),
                ('subscription', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='subscriptions.subscription')),
            ],
        ),
    ]
