from rest_framework.permissions import BasePermission
from models.py import StudioMembership

class IsStudioMember(BasePermission):
    def have_permission(self,request,view):
        studio_id = view.kwargs.get('studio_id')

        return StudioMembership.objects.filter(
            user=request.user, 
            studio_id=studio_id
        ).exists()

class IsAdminOrLead(BasePermission):
    def have_permission(self,request,view):
        studio_id = view.kwargs.get('studio_id')

        return StudioMembership.objects.filter(
            user=request.user,
            studio_id=studio_id,
            role__in= ['ADMIN','LEAD']
        ).exists()

