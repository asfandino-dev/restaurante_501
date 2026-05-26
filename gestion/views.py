from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Cliente, Empleado, Mesa, Plato, Orden, Factura, Rol, Permiso, DetalleOrden
from .forms import ClienteForm, EmpleadoForm, MesaForm, PlatoForm, OrdenForm, FacturaForm, DetalleOrdenForm
from .utils import role_required, RoleRequiredMixin

@login_required
@role_required(['Administrador'])
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

@login_required
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
 
@login_required
@role_required(['Administrador', 'Mesero'])
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'gestion/clientes.html', {'clientes': clientes})
 
@login_required
@role_required(['Administrador'])
def lista_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'gestion/empleados.html', {'empleados': empleados})
 
@login_required
@role_required(['Administrador', 'Mesero'])
def lista_mesas(request):
    mesas = Mesa.objects.all()
    return render(request, 'gestion/mesas.html', {'mesas': mesas})
 
@login_required
@role_required(['Administrador', 'Mesero'])
def lista_platos(request):
    platos = Plato.objects.all()
    return render(request, 'gestion/platos.html', {'platos': platos})
 
@login_required
@role_required(['Administrador', 'Mesero', 'Cajero'])
def lista_ordenes(request):
    ordenes = Orden.objects.all()
    return render(request, 'gestion/ordenes.html', {'ordenes': ordenes})
 
@login_required
@role_required(['Administrador', 'Cajero'])
def lista_facturas(request):
    facturas = Factura.objects.all()
    return render(request, 'gestion/facturas.html', {'facturas': facturas})

# --- CLIENTE CRUD ---
class ClienteCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ['Administrador', 'Mesero'] # Rol añadido
    model = Cliente
    form_class = ClienteForm
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_clientes')

class ClienteUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ['Administrador', 'Mesero'] # Rol añadido para corregir errores de tipeo
    model = Cliente
    form_class = ClienteForm
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_clientes')

class ClienteDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ['Administrador'] # Se mantiene exclusivo del admin
    model = Cliente
    template_name = 'gestion/confirmar_eliminar.html'
    success_url = reverse_lazy('lista_clientes')

# --- EMPLEADO CRUD ---
class EmpleadoCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ['Administrador']
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_empleados')

class EmpleadoUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ['Administrador']
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_empleados')

class EmpleadoDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ['Administrador']
    model = Empleado
    template_name = 'gestion/confirmar_eliminar.html'
    success_url = reverse_lazy('lista_empleados')

# --- MESA CRUD ---
class MesaCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ['Administrador']
    model = Mesa
    form_class = MesaForm
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_mesas')

class MesaUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ['Administrador']
    model = Mesa
    form_class = MesaForm
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_mesas')

class MesaDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ['Administrador']
    model = Mesa
    template_name = 'gestion/confirmar_eliminar.html'
    success_url = reverse_lazy('lista_mesas')

# --- PLATO CRUD ---
class PlatoCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ['Administrador']
    model = Plato
    form_class = PlatoForm
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_platos')

class PlatoUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ['Administrador']
    model = Plato
    form_class = PlatoForm
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_platos')

class PlatoDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ['Administrador']
    model = Plato
    template_name = 'gestion/confirmar_eliminar.html'
    success_url = reverse_lazy('lista_platos')

# --- ORDEN CRUD ---
class OrdenCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ['Administrador', 'Mesero']
    model = Orden
    form_class = OrdenForm
    template_name = 'gestion/form_generico.html'

    def get_success_url(self):
        return reverse_lazy('agregar_detalle', kwargs={'pk': self.object.pk})

class OrdenUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ['Administrador', 'Mesero']
    model = Orden
    form_class = OrdenForm
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_ordenes')

class OrdenDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ['Administrador']
    model = Orden
    template_name = 'gestion/confirmar_eliminar.html'
    success_url = reverse_lazy('lista_ordenes')

# --- FACTURA CRUD ---
class FacturaCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ['Administrador', 'Cajero']
    model = Factura
    form_class = FacturaForm
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_facturas')

class FacturaUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ['Administrador', 'Cajero']
    model = Factura
    form_class = FacturaForm
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_facturas')

class FacturaDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ['Administrador']
    model = Factura
    template_name = 'gestion/confirmar_eliminar.html'
    success_url = reverse_lazy('lista_facturas')


# --- REPORTE GENERAL ---
@login_required
@role_required(['Administrador'])
def reporte_general(request):
    context = {
        'total_ordenes': Orden.objects.count(),
        'total_facturas': Factura.objects.count(),
    }
    return render(request, 'gestion/reporte_general.html', context)

# --- ROLES CRUD ---
@login_required
@role_required(['Administrador'])
def lista_roles(request):
    roles = Rol.objects.all()
    return render(request, 'gestion/roles.html', {'roles': roles})

class RolCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ['Administrador']
    model = Rol
    fields = ['nombre', 'descripcion', 'permisos']
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_roles')

class RolUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ['Administrador']
    model = Rol
    fields = ['nombre', 'descripcion', 'permisos']
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_roles')

class RolDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ['Administrador']
    model = Rol
    template_name = 'gestion/confirmar_eliminar.html'
    success_url = reverse_lazy('lista_roles')

# --- PERMISOS CRUD ---
@login_required
@role_required(['Administrador'])
def lista_permisos(request):
    permisos = Permiso.objects.all()
    return render(request, 'gestion/permisos.html', {'permisos': permisos})

class PermisoCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ['Administrador']
    model = Permiso
    fields = ['nombre', 'descripcion']
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_permisos')

class PermisoUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ['Administrador']
    model = Permiso
    fields = ['nombre', 'descripcion']
    template_name = 'gestion/form_generico.html'
    success_url = reverse_lazy('lista_permisos')

class PermisoDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ['Administrador']
    model = Permiso
    template_name = 'gestion/confirmar_eliminar.html'
    success_url = reverse_lazy('lista_permisos')


@login_required
@role_required(['Administrador', 'Mesero'])
def agregar_detalle(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    
    if request.method == 'POST':
        form = DetalleOrdenForm(request.POST)
        if form.is_valid():
            # Creamos la instancia, asignamos la orden y guardamos.
            # El modelo se encargará de calcular precios y subtotales en su propio método save()
            detalle = form.save(commit=False)
            detalle.orden = orden
            detalle.save() 
            
            # Actualizamos el total de la orden (método en el modelo Orden)
            orden.update_total() 
            
            return redirect('agregar_detalle', pk=pk)
    else:
        form = DetalleOrdenForm()
        
    detalles = DetalleOrden.objects.filter(orden=orden)
    return render(request, 'gestion/agregar_detalle.html', {
        'orden': orden,
        'detalles': detalles,
        'form': form
    })

@login_required
@role_required(['Administrador', 'Mesero'])
def finalizar_orden(request, pk):
    from decimal import Decimal
    from django.contrib import messages
    from .models import DetalleOrden, Factura

    orden = get_object_or_404(Orden, pk=pk)

    # BLOQUEO: si ya fue facturada no permitir repetir
    if orden.estado_orden == 'Facturada':
        messages.error(request, 'Esta orden ya fue facturada.')
        return redirect('lista_ordenes')

    # Validar detalles
    detalles = DetalleOrden.objects.filter(orden=orden)

    if not detalles.exists():
        messages.error(request, 'La orden no tiene platos agregados.')
        return redirect('agregar_detalle', pk=pk)

    subtotal = sum(
        (d.subtotal for d in detalles if d.subtotal is not None),
        Decimal('0.00')
    )

    impuesto = (
        subtotal * Decimal('0.19')
    ).quantize(Decimal('0.01'))

    total = (
        subtotal + impuesto
    ).quantize(Decimal('0.01'))

    factura = Factura.objects.create(
        orden=orden,
        subtotal=subtotal,
        impuesto=impuesto,
        total_factura=total,
        metodo_pago='Efectivo'
    )

    # Cambiar estado
    orden.estado_orden = 'Facturada'
    orden.save()

    messages.success(request, 'Factura generada correctamente.')

    return redirect('lista_facturas')

# --- MANEJADORES DE ERRORES ---
def error_403(request, exception=None):
    """
    Captura las excepciones PermissionDenied y renderiza la plantilla 403 personalizada.
    """
    return render(request, 'gestion/403.html', status=403)