from django.db import models

# Create your models here.
class AES(models.Model):
    AES_name=models.CharField(max_length=100)
    AES_email=models.EmailField(max_length=100)
    #AES_otp=models.IntegerField()
   # profile_img=models.ImageField(upload_to="pics")