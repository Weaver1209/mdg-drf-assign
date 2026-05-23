from rest_framework import serializers
from .models import Tag,Comment,Attachment,Notification
class TagSerializer(serializers.ModelSerializer):
        class Meta:
                model = Tag
                fields = "__all__" 
class CommentSerializer(serializers.ModelSerializer):
        class Meta:
                model = Comment
                fields = '__all__'
class AttachmentSerializer(serializers.ModelSerializer):
        class Meta:
                model = Attachment
                fields = "__all__"    
class NotificationSerializer(serializers.ModelSerializer):
        class Meta:
                model = Notification
                fields = "__all__"                         