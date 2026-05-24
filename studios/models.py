from django.db import models
from django.contrib.auth.models import User

class Role(models.TextChoices):
    STUDIO_ADMIN = 'ADMIN', 'Studio Admin'
    PROJECT_LEAD = 'LEAD', 'Project Lead'
    DESIGNER = 'DESIGNER', 'Designer'
    WRITER = 'WRITER', 'Writer'
    REVIEWER = 'REVIEWER', 'Reviewer'
    CLIENT_VIEWER = 'VIEWER', 'Client Viewer'

class Studio(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank= True,null = True)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
<<<<<<< HEAD
        return self.name
class StudioMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=10, 
        choices=Role.choices, 
    )
    class Meta:
        unique_together = ('user', 'studio') 
=======
            return self.name
>>>>>>> stun

    def __str__(self):
        return f"{self.user.username} in {self.studio.name} ({self.get_role_display()})"