# Generated by Django 2.1 on 2018-11-14 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0018_auto_20181108_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientprofile',
            name='stripe_customer_id',
            field=models.CharField(default='None', max_length=200),
        ),
    ]