# Generated by Django 2.1 on 2018-11-14 21:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0020_clientprofile_stripe_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientprofile',
            name='stripe_token',
        ),
    ]