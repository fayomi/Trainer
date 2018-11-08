# Generated by Django 2.1 on 2018-11-08 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0016_remove_workout_stripe_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainerprofile',
            name='stripe_pub_key',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='trainerprofile',
            name='stripe_secret_key',
            field=models.CharField(max_length=200, null=True),
        ),
    ]