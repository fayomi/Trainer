# Generated by Django 2.1 on 2018-11-05 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0019_order_stripe_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='stripe_plan_id',
            field=models.CharField(default='None', max_length=200),
        ),
    ]
