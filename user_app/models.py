from django.db import models

# Create your models here.
class Register_Tb(models.Model):
    name=models.CharField(max_length=50)
    gender=models.CharField(max_length=20)
    dob=models.CharField(max_length=30)
    mobile=models.CharField(max_length=20)
    user_name=models.CharField(max_length=50)
    password=models.CharField(max_length=20)

