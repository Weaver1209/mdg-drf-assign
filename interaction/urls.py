from rest_framework.routers import DefaultRouter
from django.urls import path,include

from .views import TagViewSet,CommentViewSet,AttachmentViewSet,NotificationViewSet

router = DefaultRouter()
router.register(r'tags',TagViewSet)
router.register(r'comments',CommentViewSet)
router.register(r'attachments',AttachmentViewSet)
router.register(r'notifications',NotificationViewSet)
urlpatterns = [
    path('',include(router.urls)),
]