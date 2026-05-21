from rest_framework import viewsets
from .models import Tag,Comment
from .serializers import TagSerializer,CommentSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all() #here we tell which data it can interact with here we are allowing it for whole of the data
    serializer_class = TagSerializer #here we define which serializer to use for python object and json object interconversion
class CommentViewSet(viewsets.ModelViewSet):
     queryset = Comment.objects.all()
     serializer_class = CommentSerializer
     
     #on receiving the request initializing the author of the comment as the user 
     def perform_create(self, serializer):
        serializer.save(author=self.request.user)