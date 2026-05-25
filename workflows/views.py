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
from interaction.models import Notification
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
    filterset_fields = ['priority', 'stage','assignee']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'deadline', 'priority', 'stage']

    def get_permissions(self):
        return [IsAuthenticated(), IsStudioMemberOrViewerReadOnly()]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        project__studio_id = self.kwargs.get('studio_id')
        return Task.objects.filter(project_id=project_id,project__studio_id = project__studio_id)

    def perform_create(self, serializer):
        task = serializer.save(project_id=self.kwargs.get('project_id'))

        if task.assignee and task.assignee != self.request.user:
            Notification.objects.create(
                receiver=task.assignee,
                notification_type='task_assigned',
                message=f"You have been assigned to the task: '{task.title}'"
            )

    def perform_update(self, serializer):
        old_task = self.get_object()
        old_stage = old_task.stage
        old_assignee = old_task.assignee
        task = serializer.save()
        if old_stage != task.stage:
            if task.assignee:
                Notification.objects.create(
                    receiver=task.assignee,
                    notification_type='status_changed',
                    message=f"The status of task '{task.title}' has changed from {old_stage} to {task.stage}."
                )    
        if task.assignee and old_assignee != task.assignee and task.assignee != self.request.user:
            Notification.objects.create(
                receiver=task.assignee,
                notification_type='task_assigned',
                message=f"You have been assigned to the task: '{task.title}'"
            )           

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['stage', 'priority', 'assignee']
    search_fields = ['title', 'description']