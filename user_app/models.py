from django.db import models

# Create your models here.
class Register_Tb(models.Model):
    name=models.CharField(max_length=50)
    gender=models.CharField(max_length=20)
    dob=models.CharField(max_length=30)
    mobile=models.CharField(max_length=20)
    user_name=models.CharField(max_length=50)
    password=models.CharField(max_length=20)

class Message_Tb(models.Model):
    sender_id=models.ForeignKey(Register_Tb,on_delete=models.CASCADE)
    recipient_id=models.CharField(max_length=50)
    subject=models.CharField(max_length=100,default="No Subject")
    message=models.CharField(max_length=200)
    attachment=models.FileField(upload_to='thunder', blank=True, null=True, default='default.png')
    date=models.CharField(max_length=20)
    time=models.CharField(max_length=20)
    status_reciever=models.CharField(max_length=20,default='unread')
    status_sender=models.CharField(max_length=20,default='none')
