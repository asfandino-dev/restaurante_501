from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Cliente, Empleado, Mesa, Plato, Orden, Factura
from .forms import ClienteForm, EmpleadoForm, MesaForm, PlatoForm, OrdenForm, FacturaForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = UserCreationForm()
    return render(request, 'gestion/register.html', {'form': form})

def inicio(request):
    context = {
        'total_clientes': Cliente.objects.count(),
        'total_empleados': Empleado.objects.count(),
        'total_mesas': Mesa.objects.count(),
        'total_platos': Plato.objects.count(),
        'total_ordenes': Orden.objects.count(),
        'total_facturas': Factura.objects.count(),
    }
    return render(request, 'gestion/inicio.html', context)
 
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'gestion/clientes.html', {'clientes': clientes})
 
def lista_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'gestion/empleados.html', {'empleados': empleados})
 
def lista_mesas(request):
    mesas = Mesa.objects.all()
    return render(request, 'gestion/mesas.html', {'mesas': mesas})
 
def lista_platos(request):
    platos = Plato.objects.all()
    return render(request, 'gestion/platos.html', {'platos': platos})
 
def lista_ordenes(request):
    ordenes = Orden.objects.all()
    return render(request, 'gestion/ordenes.html', {'ordenes': ordenes})
 
def lista_facturas(request):
    facturas = Factura.objects.all()
    return render(request, 'gestion/facturas.html', {'facturas': facturas})
# --- CLIENTE CRUD ---
class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_clientes')

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_clientes')

class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'gestion/confirmar_eliminar.html'
    success_url = reverse_lazy('lista_clientes')

# --- EMPLEADO CRUD ---
class EmpleadoCreateView(LoginRequiredMixin, CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_empleados')

class EmpleadoUpdateView(LoginRequiredMixin, UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_empleados')

class EmpleadoDeleteView(LoginRequiredMixin, DeleteView):
    model = Empleado
    template_name = 'gestion/confirmar_eliminar.html'
    success_url = reverse_lazy('lista_empleados')

# --- MESA CRUD ---
class MesaCreateView(LoginRequiredMixin, CreateView):
    model = Mesa
    form_class = MesaForm
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_mesas')

class MesaUpdateView(LoginRequiredMixin, UpdateView):
    model = Mesa
    form_class = MesaForm
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_mesas')

class MesaDeleteView(LoginRequiredMixin, DeleteView):
    model = Mesa
    template_name = 'gestion/confirmar_eliminar.html'
    success_url = reverse_lazy('lista_mesas')

# --- PLATO CRUD ---
class PlatoCreateView(LoginRequiredMixin, CreateView):
    model = Plato
    form_class = PlatoForm
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_platos')

class PlatoUpdateView(LoginRequiredMixin, UpdateView):
    model = Plato
    form_class = PlatoForm
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_platos')

class PlatoDeleteView(LoginRequiredMixin, DeleteView):
    model = Plato
    template_name = 'gestion/confirmar_eliminar.html'
    success_url = reverse_lazy('lista_platos')

# --- ORDEN CRUD ---
class OrdenCreateView(LoginRequiredMixin, CreateView):
    model = Orden
    form_class = OrdenForm
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_ordenes')

class OrdenUpdateView(LoginRequiredMixin, UpdateView):
    model = Orden
    form_class = OrdenForm
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_ordenes')

class OrdenDeleteView(LoginRequiredMixin, DeleteView):
    model = Orden
    template_name = 'gestion/confirmar_eliminar.html'
    success_url = reverse_lazy('lista_ordenes')

# --- FACTURA CRUD ---
class FacturaCreateView(LoginRequiredMixin, CreateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_facturas')

class FacturaUpdateView(LoginRequiredMixin, UpdateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_facturas')

class FacturaDeleteView(LoginRequiredMixin, DeleteView):
    model = Factura
    template_name = 'gestion/confirmar_eliminar.html'
    success_url = reverse_lazy('lista_facturas')
