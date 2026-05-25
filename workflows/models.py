from django.db import models
from studios.models import Studio
from django.contrib.auth.models import User


class WorkflowStage(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    REVIEW = 'REVIEW', 'Review'
    REVISION = 'REVISION', 'Revision'
    APPROVED = 'APPROVED', 'Approved'
    COMPLETED = 'COMPLETED', 'Completed'


class Priority(models.TextChoices):
    LOW = 'LOW', 'Low'
    MEDIUM = 'MED', 'Medium'
    HIGH = 'HIGH', 'High'
    URGENT = 'URG', 'Urgent'
class Project(models.Model):
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    stage = models.CharField(
        max_length=10, 
        choices=WorkflowStage.choices, 
        default=WorkflowStage.DRAFT
    )
    priority = models.CharField(
        max_length=5, 
        choices=Priority.choices, 
        default=Priority.MEDIUM
    )
    
    assignee = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, blank=True
    )
    deadline = models.DateTimeField(null=True, blank=True)
    tags = models.ManyToManyField(
        'interaction.Tag',
        related_name='tasks',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title