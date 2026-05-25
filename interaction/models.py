from django.db import models
from django.contrib.auth.models import User
from studios.models import Studio

from workflows.models import Task
# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50) #charfield where two different tags can have same name
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
        unique_together = ('name', 'studio')
class Comment(models.Model):
        
        task_id = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments',null=True, blank=True)
        author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments') #linking the comments with the user data table
        parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='replies') #there can be replies for some comments so we are linking those replies with a parent comment
        content = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
             return f"Comment by {self.author.username}"
def upload_path(attachment, filename):
    return f"attachments/task_{attachment.task_id}/{filename}"        
class Attachment(models.Model): 
      
      #first linking the attachment to a particular user 
      uploaded_by = models.ForeignKey(User,null=True,on_delete=models.SET_NULL,related_name='attachments') #when the user is deleted we don't want the files also to be deleted we will just set the uploaded_by to NULL
      
      label = models.CharField( max_length=100, blank=True)
      
      file_size = models.PositiveIntegerField(null=True,blank=True)
      
      #any attachment has a particular file_type
      file_type = models.CharField(max_length=20,choices= [
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Document'),
        ('other', 'Other'),
        ],
        default='other')  
      
      created_at = models.DateTimeField(auto_now_add=True)
      
      #to connect this attachment to a particular task with foreign key, will later connect once the task model will be created
      task_id = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments', null=True, blank=True)
      file  = models.FileField(upload_to= upload_path,null = True,blank=True) #Filefield is used to store the uploaded files and the store the path of the file in your database 


      def __str__(self):
           return self.label
      
class Notification(models.Model):
           
           receiver = models.ForeignKey(User, on_delete=models.CASCADE,related_name='notifications')
           
           notification_type = models.CharField(max_length=50,choices= [
                                                    ('comment_added', 'Comment Added'),
                                                    ('task_assigned', 'Task Assigned'),
                                                    ('status_changed', 'Status Changed'),
                                                    ('review_requested', 'Review Requested'),
                                                    ])
           message = models.TextField()

           is_read = models.BooleanField(default = False)

           created_at = models.DateTimeField(auto_now_add=True)

           def __str__(self):
                 return f"Notification for {self.receiver.username}"