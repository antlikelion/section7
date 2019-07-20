from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # object단위 퍼미션
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
