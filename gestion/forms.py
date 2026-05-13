from django import forms
from .models import Cliente, Empleado, Mesa, Plato, Orden, Factura, DetalleOrden

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'correo']

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'cargo', 'telefono', 'correo']

class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ['numero_mesa', 'capacidad', 'estado_mesa']

class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre_plato', 'descripcion', 'precio', 'categoria', 'disponible']

class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['cliente', 'empleado', 'mesa', 'estado_orden']

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['orden', 'subtotal', 'impuesto', 'total_factura', 'metodo_pago']

class DetalleOrdenForm(forms.ModelForm):
    class Meta:
        model = DetalleOrden
        fields = ['plato', 'cantidad']
