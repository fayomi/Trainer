# Generated by Django 2.1 on 2018-09-30 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='trainer',
            field=models.CharField(default='none', max_length=250),
        ),
    ]
