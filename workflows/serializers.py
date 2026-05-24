from .models import Project,Task
from rest_framework import serializers

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
        fields = ['id', 'studio', 'name', 'description', 'created_by', 'created_at']
        read_only_fields = ['created_by']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'project', 'title', 'description', 'stage', 'priority', 
                  'assignee', 'deadline', 'created_at', 'updated_at']
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