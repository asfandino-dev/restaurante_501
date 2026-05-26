from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.views import redirect_to_login
from functools import wraps

def role_required(allowed_roles):
    """
    Decorator for function-based views that checks if the user has one of the allowed roles.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())

            if not hasattr(request.user, 'empleado') or request.user.empleado.cargo not in allowed_roles:
                if request.user.is_superuser and 'Administrador' in allowed_roles:
                     return view_func(request, *args, **kwargs)
                raise PermissionDenied

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

class RoleRequiredMixin(AccessMixin):
    """
    Mixin for class-based views that checks if the user has one of the allowed roles.
    """
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        user_role = getattr(request.user.empleado, 'cargo', None) if hasattr(request.user, 'empleado') else None

        # Superuser bypass for Administrador role
        if request.user.is_superuser and 'Administrador' in self.allowed_roles:
            return super().dispatch(request, *args, **kwargs)

        if user_role not in self.allowed_roles:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)
