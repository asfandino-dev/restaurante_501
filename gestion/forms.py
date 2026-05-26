from django import forms
from django.core.exceptions import ValidationError
from .models import Cliente, Empleado, Mesa, Plato, Orden, Factura, DetalleOrden

# 1. Widget reutilizable para el frontend
TELEFONO_WIDGET = forms.TextInput(attrs={
    'placeholder': '3001234567',
    'maxlength': '10',
    'oninput': "this.value = this.value.replace(/[^0-9]/g, '');",
    'style': "background-image: url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='45' height='40'><text x='10' y='25' fill='%23888' font-family='sans-serif' font-weight='bold'>+57</text></svg>\"); background-repeat: no-repeat; padding-left: 50px; border-left: 4px solid #00c853;"
})

# 2. Función de validación reutilizable para el backend
def validar_telefono_colombiano(telefono):
    if not telefono:
        return telefono
        
    numeros = ''.join(filter(str.isdigit, str(telefono)))

    if len(numeros) == 12 and numeros.startswith('57'):
        numeros = numeros[2:]

    if len(numeros) != 10:
        raise ValidationError("Un número celular colombiano debe tener exactamente 10 dígitos.")

    return f"+57 {numeros}"


# --- FORMULARIOS ---

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'correo']
        widgets = {
            'telefono': TELEFONO_WIDGET
        }
        help_texts = {
            'telefono': '🇨🇴 Ingrese solo los 10 dígitos. El indicativo se guardará automáticamente.',
        }

    def clean_telefono(self):
        return validar_telefono_colombiano(self.cleaned_data.get('telefono'))


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['user', 'nombre', 'rol', 'telefono', 'correo']
        widgets = {
            'telefono': TELEFONO_WIDGET
        }
        help_texts = {
            'telefono': '🇨🇴 Ingrese solo los 10 dígitos. El indicativo se guardará automáticamente.',
        }

    def clean_telefono(self):
        return validar_telefono_colombiano(self.cleaned_data.get('telefono'))


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


from decimal import Decimal

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['orden', 'subtotal', 'impuesto', 'total_factura', 'metodo_pago']
        widgets = {
            'subtotal': forms.NumberInput(attrs={
                'readonly': 'readonly', 
                'style': 'background-color: var(--bg-hover); color: var(--text-muted); cursor: not-allowed;'
            }),
            'impuesto': forms.NumberInput(attrs={
                'readonly': 'readonly', 
                'style': 'background-color: var(--bg-hover); color: var(--text-muted); cursor: not-allowed;'
            }),
            'total_factura': forms.NumberInput(attrs={
                'readonly': 'readonly', 
                'style': 'background-color: var(--bg-hover); color: var(--text-muted); cursor: not-allowed;'
            }),
            'orden': forms.Select(attrs={
                'style': 'background-color: var(--bg-hover); pointer-events: none;'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        orden = cleaned_data.get('orden')
        
        if orden:
            subtotal_calculado = orden.total if hasattr(orden, 'total') else Decimal('0.00')
            impuesto_calculado = (subtotal_calculado * Decimal('0.19')).quantize(Decimal('0.01'))
            total_calculado = (subtotal_calculado + impuesto_calculado).quantize(Decimal('0.01'))

            cleaned_data['subtotal'] = subtotal_calculado
            cleaned_data['impuesto'] = impuesto_calculado
            cleaned_data['total_factura'] = total_calculado

            self.instance.subtotal = subtotal_calculado
            self.instance.impuesto = impuesto_calculado
            self.instance.total_factura = total_calculado
            
        return cleaned_data


class DetalleOrdenForm(forms.ModelForm):
    class Meta:
        model = DetalleOrden
        fields = ['plato', 'cantidad']