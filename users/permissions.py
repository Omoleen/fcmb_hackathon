from rest_framework.permissions import IsAuthenticated


class IsAgent(IsAuthenticated):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            if request.user.is_agent:
                return True
        return False