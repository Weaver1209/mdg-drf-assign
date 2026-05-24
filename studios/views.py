from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Studio, StudioMembership
from .serializers import StudioSerializer, UserSerializer, StudioMembershipSerializer
from .permissions import IsStudioMember, IsAdminOrLead
from rest_framework.decorators import action
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    @action(detail=False, methods=['get'])
    def me(self, request):
        if request.user.is_authenticated:
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
class StudioViewSet(viewsets.ModelViewSet):
    serializer_class = StudioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Studio.objects.filter(studiomembership__user=self.request.user)
        
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
        )

class StudioMembershipViewSet(viewsets.ModelViewSet):
    queryset = StudioMembership.objects.all()
    serializer_class = StudioMembershipSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsStudioMember()]
        return [IsAuthenticated(), IsAdminOrLead()]
        
    def get_queryset(self):
        studio_id = self.kwargs.get('studio_id')
        if studio_id:
            return StudioMembership.objects.filter(studio_id=studio_id)
        return StudioMembership.objects.none()