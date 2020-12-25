from django.db import models


# Create your models here.
class Status(models.Model):
    timestamp = models.IntegerField()
    current_moisture = models.IntegerField()
    target_moisture = models.IntegerField()
    mode = models.CharField(max_length=6)
    relay_target_status = models.CharField(max_length=3)
    relay_current_state = models.CharField(max_length=3)
