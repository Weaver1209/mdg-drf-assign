from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from studios.models import StudioMembership
from studios.permissions import IsStudioMember, IsAdminOrLead
from .models import Project, Task, WorkflowStage
from .serializers import ProjectSerializer, TaskSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsStudioMember()]
        return [IsAuthenticated(), IsAdminOrLead()]

    def get_queryset(self):
        studio_id = self.kwargs.get('studio_id')
        return Project.objects.filter(studio_id=studio_id)

    def perform_create(self, serializer):
        serializer.save(
            studio_id=self.kwargs.get('studio_id'),
            created_by=self.request.user
        )

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_permissions(self):
        return [IsAuthenticated(), IsStudioMember()]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return Task.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        serializer.save(project_id=self.kwargs.get('project_id'))