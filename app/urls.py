from django.urls import path
from . import views  

urlpatterns = [
    path('', views.registrar_tabla, name='tabla'),  
    path('registrar/', views.registrar, name='registrar'),  

]
