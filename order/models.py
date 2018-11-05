from django.db import models


class Order(models.Model):
    #this will take information from the stripe form
    client_name = models.CharField(max_length=250, default='none')
    trainer_name = models.CharField(max_length=250, default='none') #new addition
    token = models.CharField(max_length=250,blank=True)
    total = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='GBP Order Gross Total')
    net_pay = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='GBP Order Net Total', default=0.00)
    stripe_fee = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='Stripe Fee', default=0.00)
    platform_fee = models.IntegerField(default=2)
    service_fee = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='Total Service Fee', default=0.00)
    client_email = models.EmailField(max_length=250,blank=True,verbose_name='Client Email')
    trainer_email = models.EmailField(max_length=250,blank=True,verbose_name='Trainer Email')
    created = models.DateTimeField(auto_now_add=True)
    subscription = models.BooleanField(default=False)
    stripe_product_id = models.CharField(max_length=200,default='None')
    stripe_plan_id = models.CharField(max_length=200,default='None')


    class Meta:
        db_table = 'Order'
        ordering = ['-created'] #to have the most recent order come up first

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    workout = models.CharField(max_length=250)
    sessions = models.IntegerField(default=0)
    trainer_id = models.CharField(max_length=250, default='none')
    client_id = models.CharField(max_length=250, default='none')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='GBP Price')
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    workout_description = models.TextField(default='There is no description available')

    class Meta:
        db_table = 'OrderItem'
        ordering = ['-id'] #to have the most recent order come up first

    def sub_total(self):
        return self.quantity * self.price

    def __str__(self):
        return self.workout
