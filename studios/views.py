from rest_framework import viewsets
from .models import Studio
from .serializers import StudioSerializer, UserSerializer, StudioMembershipSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

class StudioViewSet(viewsets.ModelViewSet):
    serializer_class = StudioSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Studio.objects.filter(members__user=self.request.use
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsStudioMember()]
        return [IsAuthenticated(), IsAdminOrLead()]
    def perform_create(self, serializer):
        studio = serializer.save()
        StudioMembership.objects.create(
            user=self.request.user,
            studio=studio,
            role='ADMIN'

class StudioMembershipViewSet(viewsets.ModelViewSet):
    queryset = StudioMembership.objects.all()
    serializer_class = StudioMembershipSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsStudioMember()]
        return [IsAuthenticated(), IsStudioAdminOrLead()]
    def get_queryset(self):
        studio_id = self.kwargs.get('studio_id')
        if studio_id:
            return StudioMembership.objects.filter(studio_id=studio_id)
        return StudioMembership.objects.none()