from django.shortcuts import render

def registrar_tabla(request):
    return render(request, "index.html")

def registrar(request):
    return render(request, "cliente_forms.html")

from django.shortcuts import render, redirect
from .models import Cliente

def registrar_cliente(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido_paterno = request.POST['apellidoPaterno']
        apellido_materno = request.POST['apellidoMaterno']
        dni = request.POST['dni']
        servicio = request.POST['servicio']
        fecha_inicio = request.POST['fechaInicio']
        direccion = request.POST['direccion']
        
        cliente = Cliente(
            nombre=nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            dni=dni,
            servicio=servicio,
            fecha_inicio=fecha_inicio,
            direccion=direccion
        )
        cliente.save()
        
        return redirect('success')
    return render(request, 'cliente_forms.html')










