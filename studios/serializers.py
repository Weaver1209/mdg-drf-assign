from rest_framework import serializers
from .models import Studio,StudioMembership
from db.contrib.auth.models import User

class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
<<<<<<< HEAD
        fields = ['id', 'name', 'description', 'created_at']
class StudioMembershipSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source = 'user.username')
    class Meta:
        model = StudioMembership
        fields = ['id','username','user','studio','role']
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
=======
        fields = ['id', 'name', 'description', 'created_at'] 
>>>>>>> stun
