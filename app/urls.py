from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_clientes, name='listar_clientes'),
    path('registrar/', views.registrar_cliente, name='registrar_cliente'),  
    path('eliminar/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('pagar/<int:pk>/', views.pagar_deuda, name='pagar_deuda'),
    path('informe/<int:pk>/', views.ver_informe, name='ver_informe'),
    path('clientes/informe/<int:pk>/descargar_pdf/', views.descargar_informe_pdf, name='descargar_informe_pdf'),


]

