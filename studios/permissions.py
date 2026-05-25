from rest_framework.permissions import BasePermission
from .models import StudioMembership
from rest_framework.permissions import SAFE_METHODS
class IsStudioMember(BasePermission):
    def has_permission(self,request,view):
        studio_id = view.kwargs.get('studio_id')
        if not studio_id:
            studio_id = view.kwargs.get('pk')
            
        if not studio_id:
            return True 

        return StudioMembership.objects.filter(
            user=request.user, 
            studio_id=studio_id
        ).exists()

class IsAdminOrLead(BasePermission):

    def has_permission(self,request,view):
        studio_id = view.kwargs.get('studio_id')
        if not studio_id:
            studio_id = view.kwargs.get('pk') # Fallback for top-level studio URLs
            
        if not studio_id:
            return True
        return StudioMembership.objects.filter(
            user=request.user,
            studio_id=studio_id,
            role__in= ['ADMIN','LEAD']
        ).exists()
class IsStudioMemberOrViewerReadOnly(BasePermission):
    def has_permission(self, request, view):
        studio_id = view.kwargs.get('studio_id') or view.kwargs.get('pk')
        if not studio_id: return True

        membership = StudioMembership.objects.filter(
            user=request.user, studio_id=studio_id
        ).first()
        
        if not membership: return False
            
        
        if membership.role == 'VIEWER':
            return request.method in SAFE_METHODS
            
        return True

