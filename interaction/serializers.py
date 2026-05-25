from rest_framework import serializers
from .models import Tag,Comment,Attachment,Notification
class TagSerializer(serializers.ModelSerializer):
        class Meta:
                model = Tag
                fields = "__all__" 
                read_only_fields = ['created_at']
class CommentSerializer(serializers.ModelSerializer):
        class Meta:
                model = Comment
                fields = '__all__'
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