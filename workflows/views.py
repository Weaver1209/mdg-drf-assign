from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from studios.models import StudioMembership
from studios.permissions import IsStudioMember, IsAdminOrLead, IsStudioMemberOrViewerReadOnly
from .models import Project, Task, WorkflowStage
from .serializers import ProjectSerializer, TaskSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_permissions(self):
       if self.action in ['list', 'retrieve']:
        return [IsAuthenticated(), IsStudioMember()]
       if self.action == 'destroy':
        return [IsAuthenticated(), IsAdminOrLead()]
       return [IsAuthenticated(), IsStudioMemberOrViewerReadOnly()]

    def get_queryset(self):
        studio_id = self.kwargs.get('studio_id')
        return Project.objects.filter(
        studio_id=studio_id, 
        studio__studiomembership__user=self.request.user
    )

    def perform_create(self, serializer):
        serializer.save(
            studio_id=self.kwargs.get('studio_id'),
            created_by=self.request.user
        )

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['priority', 'stage']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'deadline', 'priority', 'stage']

    def get_permissions(self):
        return [IsAuthenticated(), IsStudioMemberOrViewerReadOnly()]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        project__studio_id = self.kwargs.get('studio_id')
        return Task.objects.filter(project_id=project_id,project__studio_id = project__studio_id)

    def perform_create(self, serializer):
        serializer.save(project_id=self.kwargs.get('project_id'))
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['stage', 'priority', 'assignee']
    search_fields = ['title', 'description']