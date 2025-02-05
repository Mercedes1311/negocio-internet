
from django.shortcuts import render, redirect
from .models import Cliente
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Cliente, Pago
from .forms import ClienteForm
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.templatetags.static import static



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
    clientes = Cliente.objects.all()
    query = request.GET.get('q')
    if query:
        clientes = clientes.filter(nombre__icontains=query)
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
        monto_pagado = float(request.POST['monto_pagado'])
        Pago.objects.create(cliente=cliente, monto_pagado=monto_pagado)
        return redirect('listar_clientes')
    return render(request, 'pagar_deuda.html', {'cliente': cliente})

@login_required(login_url='login')
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
@login_required(login_url='login')
def descargar_informe_pdf(request, cliente_id):
    #    # Obtener datos del cliente y pagos
    cliente = get_object_or_404(Cliente, id=cliente_id)
    pagos = Pago.objects.filter(cliente=cliente)

    # Calcular deuda actual y siguiente pago (ajusta según tu modelo)
    deuda_actual = cliente.deuda_actual if hasattr(cliente, 'deuda_actual') else "No disponible"
    siguiente_pago = cliente.siguiente_pago if hasattr(cliente, 'siguiente_pago') else "No disponible"

    # Plantilla HTML para el PDF
    template_path = 'ver_informe_pdf.html'
    context = {
        'cliente': cliente,
        'pagos': pagos,
        'deuda_actual': deuda_actual,
        'siguiente_pago': siguiente_pago
    }

    # Cargar y renderizar plantilla
    template = get_template(template_path)
    html = template.render(context)

    # Crear respuesta HTTP como PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Informe_{cliente.nombre}.pdf"'

    # Convertir HTML a PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Si hay un error en la conversión
    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)

    return response

def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return redirect('register')

        # Crear el usuario
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        # Mensaje de éxito
        messages.success(request, "¡Cuenta creada con éxito!")
        return redirect('login')  # Redirigir a la página de login después del registro
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, 'login.html')


