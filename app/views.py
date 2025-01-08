from django.shortcuts import render

def registrar_tabla(request):
    return render(request, "index.html")

def registrar(request):
    return render(request, "cliente_forms.html")










