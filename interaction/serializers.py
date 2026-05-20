from rest_framework import serializers
from .models import Tag
class TagSerializer(serializers.ModelSerializer):

        class Meta:
                models = Tag
                fields = "__all__"  