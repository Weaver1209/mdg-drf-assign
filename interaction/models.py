from django.db import models
from django.contrib.auth.models import User
from studios.models import Studio

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50,unique = True) #charfield where two different tags can have same name
    color = models.CharField(max_length=7,default="#ffffff") # to assign a colour to a particular tag having by default whtie colour 
    
    
    studio = models.ForeignKey(Studio,on_delete=models.CASCADE,related_name='tags') 
    #foreign key is used for linking between two data in two different tables
    #with the help of on_delete if the studio is deleted then all the tags mapped to that studio are also deleted
    #related name is used to creatte a reverse lookup so that we can also acccess all of the tags related to a particualr studio 
    created_at = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return self.name  #whenever we print any of the object of this class it will simply print it's name
    class Meta: 
        ordering = ['name']  #means queries return the tags in a sorted order on the basis of the name
