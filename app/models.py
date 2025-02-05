from django.db import models
from datetime import date, timedelta
from calendar import monthrange

class Cliente(models.Model):
    SERVICIO_CHOICES = [
        (30, "30"),
        (35, "35"),
        (40, "40"),
        (45, "45"),
        (50, "50"),
        (55, "55"),
    ]

    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, unique=True)
    servicio = models.DecimalField(max_digits=5, decimal_places=2, choices=SERVICIO_CHOICES)
    fecha_inicio = models.DateField()
    direccion = models.TextField()

    def deuda_actual(self):
        
        meses_transcurridos = (date.today().year - self.fecha_inicio.year) * 12 + (date.today().month - self.fecha_inicio.month)
        pagos_realizados = self.pago_set.aggregate(models.Sum('monto_pagado'))['monto_pagado__sum'] or 0
        deuda_total = meses_transcurridos * (self.servicio) - pagos_realizados
        return  max(deuda_total, 0)

    def siguiente_pago(self):
        # Obtener el mes y año del siguiente pago, ajustando al mismo día del mes
        next_month = (self.fecha_inicio.month + 1) if self.fecha_inicio.month < 12 else 1
        next_year = self.fecha_inicio.year if next_month > 1 else self.fecha_inicio.year + 1
        
        # Verificar si el siguiente mes tiene el mismo día (en caso de que el mes tenga menos días)
        try:
            siguiente_pago = date(next_year, next_month, self.fecha_inicio.day)
        except ValueError:
            # Si no existe ese día en el siguiente mes (por ejemplo, 31 de febrero), ajustamos al último día del mes
            _, last_day_of_next_month = monthrange(next_year, next_month)
            siguiente_pago = date(next_year, next_month, last_day_of_next_month)
        
        return siguiente_pago

    def tiene_pago_hoy(self):
        
        return self.siguiente_pago() == date.today()
    
    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} ({self.dni})"


class Pago(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_pago = models.DateField(auto_now_add=True)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-fecha_pago']

    def __str__(self):
        return f"Pago de {self.cliente.nombre} - {self.monto_pagado} en {self.fecha_pago}"
