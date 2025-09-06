from rest_framework import permissions

class IsPlayer(permissions.BasePermission):
    """
    Custom permission to only allow players to access an object.
    """
    def has_permission(self, request, view):
        # Assuming 'Player' is a group name
        return request.user and request.user.groups.filter(name='Player').exists()

class IsOpsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow Ops/Admin users to access an object.
    """
    def has_permission(self, request, view):
        # Assuming 'Ops/Admin' is a group name
        return request.user and request.user.groups.filter(name='Ops/Admin').exists()

class IsAuditor(permissions.BasePermission):
    """
    Custom permission to only allow Auditor users to access an object.
    """
    def has_permission(self, request, view):
        # Assuming 'Auditor' is a group name
        return request.user and request.user.groups.filter(name='Auditor').exists()

class IsOwnerOrOpsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or Ops/Admin users to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request, so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet or Ops/Admin.
        return obj.user == request.user or request.user.groups.filter(name='Ops/Admin').exists()
