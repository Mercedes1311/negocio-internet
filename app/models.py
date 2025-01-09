from django.db import models
from datetime import date, timedelta

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
        """Calcula la deuda acumulada en base a los meses no pagados."""
        meses_transcurridos = (date.today().year - self.fecha_inicio.year) * 12 + (date.today().month - self.fecha_inicio.month)
        pagos_realizados = self.pago_set.aggregate(models.Sum('monto_pagado'))['monto_pagado__sum'] or 0
        deuda_total = meses_transcurridos * float(self.servicio) - pagos_realizados
        return max(deuda_total, 0)

    def siguiente_pago(self):
        """Calcula la fecha estimada del próximo pago."""
        if self.pago_set.exists():
            ultimo_pago = self.pago_set.latest('fecha_pago')
            return ultimo_pago.fecha_pago + timedelta(days=30)
        return self.fecha_inicio + timedelta(days=30)

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
