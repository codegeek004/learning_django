# Generated by Django 5.0.9 on 2024-11-27 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0017_subscription_features'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='subtitle',
            field=models.CharField(blank=True, null=True),
        ),
    ]
