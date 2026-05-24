from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TaskViewSet

router = DefaultRouter()

router.register(
    r'studios/(?P<studio_id>[^/.]+)/projects', 
    ProjectViewSet, 
    basename='studio-projects'
)
router.register(
    r'studios/(?P<studio_id>[^/.]+)/projects/(?P<project_id>[^/.]+)/tasks', 
    TaskViewSet, 
    basename='project-tasks'
)

urlpatterns = [
    path('', include(router.urls)),
]