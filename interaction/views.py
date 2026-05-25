from rest_framework import viewsets
from .models import Tag,Comment,Attachment,Notification
from .serializers import TagSerializer,CommentSerializer,AttachmentSerializer,NotificationSerializer

from rest_framework.permissions import IsAuthenticated

from rest_framework.parsers import MultiPartParser, FormParser #we need them as endpoint accept data in the form of json data only but here the user can even upload files so we need some special parsers

#for the filtering of the database we need to import the following 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)

#for creating a custom end point need to import the following 
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from studios.permissions import IsStudioMember
# Create your views here.
class TagViewSet(viewsets.ModelViewSet):
    
    serializer_class = TagSerializer #here we define which serializer to use for python object and json object interconversion
    permission_classes = [IsAuthenticated,IsStudioMember] #restricting the permission to access to only authenticated user and the studio members only
    
    def get_queryset(self):
          studio_id = self.kwargs.get('studio_id')
          return Tag.objects.filter(
               studio_id=studio_id,
               studio__studiomembership__user=self.request.user
          )
    
    def perform_create(self, serializer):
          studio_id = self.kwargs.get('studio_id')
          serializer.save(studio_id=studio_id)
class CommentViewSet(viewsets.ModelViewSet):

     serializer_class = CommentSerializer
     permission_classes = [IsAuthenticated,IsStudioMember]

     def get_queryset(self):
          studio_id = self.kwargs.get('studio_id')
          return Comment.objects.filter(
               task_id__project__studio_id=studio_id,
               task_id__project__studio__studiomembership__user=self.request.user
          )
     filter_backends = [ DjangoFilterBackend, SearchFilter, OrderingFilter] #activates filtering , searching , and ordering for this viewset
     filterset_fields = ['task_id','author'] #to filter the database based on the task_id or author 
     search_fields = ['content'] # to search on the basis of the content
     ordering_fields = ['created_at'] #to order on the basis of the creation date

     #on receiving the request initializing the author of the comment as the user 
     def perform_create(self, serializer):
         comment = serializer.save(author=self.request.user)
         task = comment.task_id
         if task:
             if task.assignee and task.assignee != self.request.user:
                 Notification.objects.create(
                     receiver=task.assignee,
                     notification_type='comment_added',
                     message=f"{self.request.user.username} commented on your assigned task '{task.title}': \"{comment.content[:50]}...\""
                 )
             if comment.parent and comment.parent.author != self.request.user:
                 Notification.objects.create(
                     receiver=comment.parent.author,
                     notification_type='comment_added',
                     message=f"{self.request.user.username} replied to your comment on task '{task.title}'."
                 )

class AttachmentViewSet(viewsets.ModelViewSet):
      
      serializer_class = AttachmentSerializer
      
      permission_classes = [IsAuthenticated,IsStudioMember]
      
      def get_queryset(self):
           studio_id = self.kwargs.get('studio_id')
           return Attachment.objects.filter(
               task_id__project__studio_id=studio_id,
               task_id__project__studio__studiomembership__user=self.request.user
           )
      parser_classes = [MultiPartParser, FormParser] #with the help of this the endpoint can accept different files not only json objects only
      
      filter_backends = [DjangoFilterBackend]
      filterset_fields = ['task_id']

      def perform_create(self, serializer):
           serializer.save(uploaded_by = self.request.user)
class NotificationViewSet(viewsets.ModelViewSet):
      #not fetching all the notifications only fetching those related to the user and sorting them on the basis of the date of creation in a descending order 
      def get_queryset(self):
           return Notification.objects.filter(receiver = self.request.user).order_by('-created_at')
      serializer_class = NotificationSerializer
      permission_classes = [IsAuthenticated]
      
      filter_backends = [ DjangoFilterBackend,SearchFilter, OrderingFilter] 
      filterset_fields = ['is_read','notification_type'] 
      search_fields = ['message'] 
      ordering_fields = ['created_at'] 

      #creating a custom end point to mark the notification as read
      @action(detail=True, methods=['patch']) #detail = true so that we can refer to the specific notification object only
      def mark_as_read(self, request, pk = None):
               notification = self.get_object()
               notification.is_read = True                 #changing the is_read field as True 
               notification.save()
               return Response({'message': 'Notification marked as read'}) #returning a response is mandatory the status code will be returned as 200 by default by the drf
      
      
      def perform_create(self, serializer):
           serializer.save(receiver =self.request.user)
