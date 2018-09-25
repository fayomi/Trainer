from django.db import models
from gym.models import Workout
# Create your models here.


class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Cart'
        ordering = ['date_added']

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'CartItem'

    def sub_total(self):
        return self.workout.price * self.quantity

    def __str__(self):
        return self.workout
