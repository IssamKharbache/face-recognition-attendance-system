from django.db import models
from django.db.models import DateTimeField
from django.contrib.auth.models import User
from PIL import Image
from datetime import datetime
from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage
from users.storage import OverwriteStorage
# Create your models here.

    

types = [('employee','employee'),('manager','manager')]
defaultstime = [('default','0000-00-00 00:00:00')]
timeworked = [('1','default')]

class Employe(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    cin  = models.CharField(max_length=70,default='',primary_key=True)
    date = models.DateField()
    timein = models.DateTimeField(null=True)
    timeout = models.DateTimeField(null=True)
    timeworked = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)
    email = models.EmailField() 
    profession = models.CharField(choices=types,max_length=20,null=True,blank=False,default='employee')
    image = models.ImageField(default='default.jpg',storage=OverwriteStorage())

    
    def __str__(self):
        return self.first_name +' '+self.last_name
    
    def save(self, *args, **kwargs):
           if self.pk and not self.image:
             old_image = Employe.objects.get(pk=self.pk).image
             self.image = old_image  
           else:
            self.image.name = f'images/{self.cin}.jpg'
           super(Employe, self).save(*args, **kwargs)


    def delete(self,*args,**kwargs):
        self.image.delete()
        super().delete(*args,**kwargs)        
    
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    

