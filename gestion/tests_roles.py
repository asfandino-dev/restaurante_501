from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from gestion.models import Empleado
from gestion.utils import role_required, RoleRequiredMixin
from django.http import HttpResponse
from django.views import View

@role_required(['Administrador'])
def mock_admin_view(request):
    return HttpResponse("Success")

@role_required(['Mesero'])
def mock_mesero_view(request):
    return HttpResponse("Success")

class RoleRequiredTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin_user = User.objects.create_user(username='admin', password='password')
        Empleado.objects.create(user=self.admin_user, nombre='Admin', cargo='Administrador')

        self.mesero_user = User.objects.create_user(username='mesero', password='password')
        Empleado.objects.create(user=self.mesero_user, nombre='Mesero', cargo='Mesero')

        self.cajero_user = User.objects.create_user(username='cajero', password='password')
        Empleado.objects.create(user=self.cajero_user, nombre='Cajero', cargo='Cajero')

    def test_admin_access_to_admin_view(self):
        request = self.factory.get('/mock-admin/')
        request.user = self.admin_user
        response = mock_admin_view(request)
        self.assertEqual(response.status_code, 200)

    def test_mesero_denied_from_admin_view(self):
        request = self.factory.get('/mock-admin/')
        request.user = self.mesero_user
        with self.assertRaises(PermissionDenied):
            mock_admin_view(request)

    def test_mesero_access_to_mesero_view(self):
        request = self.factory.get('/mock-mesero/')
        request.user = self.mesero_user
        response = mock_mesero_view(request)
        self.assertEqual(response.status_code, 200)

    def test_cajero_denied_from_mesero_view(self):
        request = self.factory.get('/mock-mesero/')
        request.user = self.cajero_user
        with self.assertRaises(PermissionDenied):
            mock_mesero_view(request)

class MockCBV(RoleRequiredMixin, View):
    allowed_roles = ['Administrador']
    def get(self, request):
        return HttpResponse("Success")

class RoleRequiredMixinTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin_user = User.objects.create_user(username='admin', password='password')
        Empleado.objects.create(user=self.admin_user, nombre='Admin', cargo='Administrador')

        self.mesero_user = User.objects.create_user(username='mesero', password='password')
        Empleado.objects.create(user=self.mesero_user, nombre='Mesero', cargo='Mesero')

    def test_admin_access_to_cbv(self):
        request = self.factory.get('/mock-cbv/')
        request.user = self.admin_user
        view = MockCBV.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_mesero_denied_from_cbv(self):
        request = self.factory.get('/mock-cbv/')
        request.user = self.mesero_user
        view = MockCBV.as_view()
        with self.assertRaises(PermissionDenied):
            view(request)
