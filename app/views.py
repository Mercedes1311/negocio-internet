
from django.shortcuts import render, redirect
from .models import Cliente

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Cliente, Pago
from .forms import ClienteForm

# Registrar cliente
def registrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'registrar_cliente.html', {'form': form})

# Listar clientes
def listar_clientes(request):
    clientes = Cliente.objects.all()
    query = request.GET.get('q')
    if query:
        clientes = clientes.filter(nombre__icontains=query)
    return render(request, 'listar_clientes.html', {'clientes': clientes})

# Eliminar cliente
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.delete()
    return redirect('listar_clientes')

# Pagar deuda
def pagar_deuda(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        monto_pagado = float(request.POST['monto_pagado'])
        Pago.objects.create(cliente=cliente, monto_pagado=monto_pagado)
        return redirect('listar_clientes')
    return render(request, 'pagar_deuda.html', {'cliente': cliente})

def ver_informe(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    pagos = cliente.pago_set.all()
    return render(request, 'ver_informe.html', {'cliente': cliente, 'pagos': pagos})

