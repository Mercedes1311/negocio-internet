
from django.shortcuts import render, redirect
from .models import Cliente
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Cliente, Pago
from .forms import ClienteForm
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def registrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'registrar_cliente.html', {'form': form})


def listar_clientes(request):
    clientes = Cliente.objects.all()
    query = request.GET.get('q')
    if query:
        clientes = clientes.filter(nombre__icontains=query)
    notificaciones = [cliente for cliente in clientes if cliente.tiene_pago_hoy()]

    return render(request, 'listar_clientes.html', {
        'clientes': clientes,
        'notificaciones': notificaciones,
    })



def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.delete()
    return redirect('listar_clientes')


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
    deuda_actual = cliente.deuda_actual()
    siguiente_pago = cliente.siguiente_pago()
    return render(request, 'ver_informe.html', {
        'cliente': cliente,
        'pagos': pagos,
        'deuda_actual': deuda_actual,
        'siguiente_pago': siguiente_pago,
    })
def descargar_informe_pdf(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    pagos = cliente.pago_set.all()
    deuda_actual = cliente.deuda_actual()
    siguiente_pago = cliente.siguiente_pago()

    template = get_template('ver_informe_pdf.html')
    context = {
        'cliente': cliente,
        'pagos': pagos,
        'deuda_actual': deuda_actual,
        'siguiente_pago': siguiente_pago,
    }
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="informe_cliente_{cliente.id}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', content_type='text/plain')
    return response


