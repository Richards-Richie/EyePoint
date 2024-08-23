from django.db import models

class Users(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    ipaddress = models.GenericIPAddressField()

class save_gaze_data(models.Model):
    gaze_x=models.IntegerField()
    gaze_y=models.IntegerField()
