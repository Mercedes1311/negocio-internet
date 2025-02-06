# forms.py
from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido_paterno', 'apellido_materno', 'dni', 'servicio', 'fecha_inicio', 'direccion', 'deuda_manual']
