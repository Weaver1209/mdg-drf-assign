from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, StudioViewSet, StudioMembershipViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'studios', StudioViewSet,basename='studio')

router.register(r'studios/(?P<studio_id>[^/.]+)/members', StudioMembershipViewSet, basename='studio-members')

urlpatterns = [
    path('', include(router.urls)),
]