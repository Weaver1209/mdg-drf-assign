from rest_framework import viewsets
from .models import Studio
from .serializers import StudioSerializer, UserSerializer, StudioMembershipSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class StudioViewSet(viewsets.ModelViewSet):
    queryset = Studio.objects.all()
    serializer_class = StudioSerializer

class StudioMembershipViewSet(viewsets.ModelViewSet):
    queryset = StudioMembership.objects.all()
    serializer_class = StudioMembershipSerializer