from rest_framework import serializers
from .models import Tag,Comment,Attachment,Notification
class TagSerializer(serializers.ModelSerializer):
        class Meta:
                model = Tag
                fields = ['id', 'name', 'color', 'studio', 'created_at']
                read_only_fields = ['studio', 'created_at']
class CommentSerializer(serializers.ModelSerializer):
        author_username = serializers.ReadOnlyField(source = 'author.username')
        class Meta:
                model = Comment
                fields = ['id', 'task_id', 'author', 'author_username', 'content', 'created_at', 'updated_at']
                read_only_fields = ['author', 'created_at', 'updated_at']
class AttachmentSerializer(serializers.ModelSerializer):
        class Meta:
                model = Attachment
                fields = "__all__"   
                read_only_fields = ['uploaded_by', 'file_size','created_at'] 
class NotificationSerializer(serializers.ModelSerializer):
        class Meta:
                model = Notification
                fields = "__all__"     
                read_only_fields = ['recipient','created_at']                    