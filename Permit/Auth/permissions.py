from rest_framework.permissions import BasePermission, IsAuthenticated



class IsAdminUser(BasePermission):


    def has_permission(self,request,view):

        return request.user and request.user.is_superuser and request.user.is_authenticated
    
class IsRegularUser(BasePermission):

    def has_permission(self, request, view):
        return request.user and not request.user.is_superuser
    


