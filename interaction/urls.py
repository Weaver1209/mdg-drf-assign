from rest_framework.routers import DefaultRouter
from django.urls import path,include

from .views import TagViewSet,CommentViewSet

router = DefaultRouter()
router.register(r'tags',TagViewSet)
router.register(r'comments',CommentViewSet)

urlpatterns = [
    path('',include(router.urls)),
]