from rest_framework import viewsets
from .models import Tag,Comment,Attachment,Notification
from .serializers import TagSerializer,CommentSerializer,AttachmentSerializer,NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser #we need them as endpoint accept data in the form of json data only but here the user can even upload files so we need some special parsers

# Create your views here.
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all() #here we tell which data it can interact with here we are allowing it for whole of the data
    serializer_class = TagSerializer #here we define which serializer to use for python object and json object interconversion
    permission_classes = [IsAuthenticated] #restricting the permission to access to only authenticated user only
class CommentViewSet(viewsets.ModelViewSet):
     queryset = Comment.objects.all()
     serializer_class = CommentSerializer
     permission_classes = [IsAuthenticated]
     #on receiving the request initializing the author of the comment as the user 
     def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class AttachmentViewSet(viewsets.ModelViewSet):
      queryset = Attachment.objects.all()
      serializer_class = AttachmentSerializer
      
      permission_classes = [IsAuthenticated]
      
      parser_classes = [MultiPartParser, FormParser] #with the help of this the endpoint can accept different files not only json objects only

      def perform_create(self, serializer):
           serializer.save(uploaded_by = self.request.user)
class NotificationViewSet(viewsets.ModelViewSet):
      queryset = Notification.objects.all()
      serializer_class = NotificationSerializer
      permission_classes = [IsAuthenticated]
      def perform_create(self, serializer):
           serializer.save(receiver =self.request.user)