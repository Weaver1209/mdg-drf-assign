from .models import Project,Task, WorkflowStage
from rest_framework import serializers
from interaction.models import Tag
from django.contrib.auth.models import User

VALID_TRANSITIONS = {
    WorkflowStage.DRAFT: [WorkflowStage.REVIEW],
    WorkflowStage.REVIEW: [WorkflowStage.APPROVED, WorkflowStage.REVISION],
    WorkflowStage.REVISION: [WorkflowStage.REVIEW],
    WorkflowStage.APPROVED: [WorkflowStage.COMPLETED],
    WorkflowStage.COMPLETED: []
}

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['created_at'] 


class TaskSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        required=False
    )
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Task
        fields = ['id', 'project', 'title', 'description', 'stage', 'priority', 
                  'assignee', 'deadline', 'tags', 'created_at', 'updated_at']
        read_only_fields = ['project']
    def validate(self, data):
        if self.instance:
            current_stage = self.instance.stage
            new_stage = data.get('stage', current_stage) 
            if current_stage != new_stage:
                allowed_next_stages = VALID_TRANSITIONS.get(current_stage, [])
                
                if new_stage not in allowed_next_stages:
                    raise serializers.ValidationError(
                        f"Cannot move task from {current_stage} to {new_stage}. "
                    )
        
        return data
    def validate_assignee(self, value):
        if value:
            project_id = self.instance.project_id if self.instance else self.initial_data.get('project')
            project = Project.objects.get(id=project_id)
            membership = StudioMembership.objects.filter(user=value, studio=project.studio).first()
            if not membership:
                raise serializers.ValidationError("This user is not a member of this studio.")
            if membership.role == 'VIEWER':
                raise serializers.ValidationError("Cannot assign tasks to a Client Viewer.")
        return value