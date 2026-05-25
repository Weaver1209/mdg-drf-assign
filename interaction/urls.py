from rest_framework.routers import DefaultRouter
from django.urls import path,include

from .views import TagViewSet,CommentViewSet,AttachmentViewSet,NotificationViewSet

router = DefaultRouter()
router.register(r'studios/(?P<studio_id>[^/.]+)/tags', TagViewSet, basename='studio-tags')
router.register(r'studios/(?P<studio_id>[^/.]+)/comments', CommentViewSet, basename='studio-comments')
router.register(r'studios/(?P<studio_id>[^/.]+)/attachments', AttachmentViewSet, basename='studio-attachments')
router.register(r'notifications',NotificationViewSet, basename='notification')
urlpatterns = [
    path('',include(router.urls)),
]