from django.db import models
from gym.models import User

# Create your models here.
class StripeDetail(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    name = models.CharField(max_length=100,null=True)
    stripe_id = models.CharField(max_length=200,null=True)
    stripe_pub_key = models.CharField(max_length=200,null=True)
    stripe_secret_key = models.CharField(max_length=200,null=True)

    class Meta:
        db_table = 'StripeDetail'
