from rest_framework import serializers
from .models import Tag,Comment
class TagSerializer(serializers.ModelSerializer):
        class Meta:
                model = Tag
                fields = "__all__"  
class CommentSerializer(serializers.ModelSerializer):
        class Meta:
                model = Comment
                fields = '__all__'
                    