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

            # Bypass de seguridad: El superusuario tiene acceso a todo.
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # Validar el rol a través de la relación empleado -> rol -> nombre
            if hasattr(request.user, 'empleado') and request.user.empleado.rol:
                if request.user.empleado.rol.nombre in allowed_roles:
                    return view_func(request, *args, **kwargs)

            raise PermissionDenied

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

        # Bypass de seguridad: El superusuario tiene acceso a todo.
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Extracción segura del nombre del rol
        user_role = request.user.empleado.rol.nombre if hasattr(request.user, 'empleado') and request.user.empleado.rol else None

        if user_role not in self.allowed_roles:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)