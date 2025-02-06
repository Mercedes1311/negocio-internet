from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Cliente, Pago
from .forms import ClienteForm
from datetime import date


@login_required
def home_view(request):
    return render(request, 'home.html')


@login_required(login_url='login')
def registrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'registrar_cliente.html', {'form': form})

@login_required(login_url='login')
def listar_clientes(request):
    query = request.GET.get('q', '')
    clientes = list(Cliente.objects.all())  # Convertimos a lista para ordenar manualmente

    if query:
        clientes = [cliente for cliente in clientes if query.lower() in cliente.nombre.lower()]

    # Ordenar por la fecha del siguiente pago (de más lejano a más cercano)
    clientes.sort(key=lambda cliente: cliente.siguiente_pago(), reverse=False)

    # Notificaciones de pago
    notificaciones = [cliente for cliente in clientes if cliente.tiene_pago_hoy()]

    return render(request, 'listar_clientes.html', {
        'clientes': clientes,
        'notificaciones': notificaciones,
    })





@login_required(login_url='login')
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.delete()
    return redirect('listar_clientes')


@login_required(login_url='login')
def pagar_deuda(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        try:
            monto_pagado = float(request.POST['monto_pagado'])
            if monto_pagado <= 0:
                messages.error(request, "El monto debe ser mayor que 0.")
            else:
                Pago.objects.create(cliente=cliente, monto_pagado=monto_pagado)
                messages.success(request, "Pago registrado correctamente.")
                return redirect('listar_clientes')
        except ValueError:
            messages.error(request, "Monto inválido.")

    return render(request, 'pagar_deuda.html', {'cliente': cliente})


@login_required(login_url='login')
def ver_informe(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    pagos = cliente.pago_set.all()
    deuda_actual = cliente.deuda_actual()  # Se llama como método
    siguiente_pago = cliente.siguiente_pago()  # Se llama como método

    return render(request, 'ver_informe.html', {
        'cliente': cliente,
        'pagos': pagos,
        'deuda_actual': deuda_actual,
        'siguiente_pago': siguiente_pago,
    })


@login_required(login_url='login')
def descargar_informe_pdf(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    pagos = Pago.objects.filter(cliente=cliente)
    deuda_actual = cliente.deuda_actual()  # Se llama correctamente como método
    siguiente_pago = cliente.siguiente_pago()

    template_path = 'ver_informe_pdf.html'
    context = {
        'cliente': cliente,
        'pagos': pagos,
        'deuda_actual': deuda_actual,
        'siguiente_pago': siguiente_pago
    }

    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Informe_{cliente.nombre}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)

    return response


def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "¡Cuenta creada con éxito!")
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, 'login.html')
