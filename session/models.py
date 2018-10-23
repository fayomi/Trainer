from django.db import models
from order.models import Order

# Create your models here.
class Session(models.Model):


    client_id = models.CharField(max_length=250, default='none')
    trainer_id = models.CharField(max_length=250, default='none')
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    total_sessions = models.PositiveIntegerField(default=0)
    workout_name = models.CharField(max_length=250)
    status = models.CharField(max_length=250, default='available')
    # if status is completed it creates a new object of available session(1-total sessions) with updated time
    # and changes status back to pending?
    # If available sessions is 0, display, you have no active sessions
    class Meta:
        db_table = 'Session'
        ordering = ['-order'] #to have the most recent order come up first


class AvailableSession(models.Model):
    session = models.ForeignKey(Session,on_delete=models.CASCADE,related_name='availablesession')
    available_sessions = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'AvailableSession'
