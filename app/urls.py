from django.urls import path
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, login_view

urlpatterns = [
    path('', views.home_view, name='home'),
    path('listar_clientes/', views.listar_clientes, name='listar_clientes'),
    path('registrar/', views.registrar_cliente, name='registrar_cliente'),  
    path('eliminar/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('pagar/<int:pk>/', views.pagar_deuda, name='pagar_deuda'),
    path('informe/<int:pk>/', views.ver_informe, name='ver_informe'),
    path('informe-cliente/<int:cliente_id>/pdf/', views.descargar_informe_pdf, name='descargar_informe_pdf'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'), 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
    template_name="password_reset.html"), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name="password_reset_done.html"), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="password_reset_confirm.html"), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name="password_reset_complete.html"), name='password_reset_complete'),



]

