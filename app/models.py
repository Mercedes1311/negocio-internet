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
    deuda_manual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_inicio = models.DateField()
    direccion = models.TextField()

    def siguiente_pago(self):
        """Calcula la fecha del próximo pago."""
        fecha_pago = self.fecha_inicio
        hoy = date.today()

        while fecha_pago <= hoy:
            mes_siguiente = fecha_pago.month + 1 if fecha_pago.month < 12 else 1
            anio_siguiente = fecha_pago.year if mes_siguiente > 1 else fecha_pago.year + 1

            try:
                fecha_pago = date(anio_siguiente, mes_siguiente, self.fecha_inicio.day)
            except ValueError:
                _, last_day = monthrange(anio_siguiente, mes_siguiente)
                fecha_pago = date(anio_siguiente, mes_siguiente, last_day)

        return fecha_pago

    def tiene_pago_hoy(self):
        """Verifica si hoy es la fecha de pago."""
        return self.siguiente_pago() == date.today()

    def deuda_actual(self):
        """Calcula la deuda acumulada, sumando el servicio un día después del pago y restando pagos."""
        deuda_total = float(self.deuda_manual) + float(self.servicio)  # Deuda inicial

        hoy = date.today()
        fecha_pago = self.fecha_inicio

        # Obtener el último pago realizado
        ultimo_pago = self.pago_set.order_by('-fecha_pago').first()
        fecha_ultimo_pago = ultimo_pago.fecha_pago if ultimo_pago else None

        while fecha_pago + timedelta(days=1) <= hoy:
            fecha_acumulacion = fecha_pago + timedelta(days=1)  # Día después del pago

            # Sumar el servicio solo si no se ha pagado antes de esta fecha
            if not fecha_ultimo_pago or fecha_ultimo_pago < fecha_acumulacion:
                deuda_total += float(self.servicio)

            # Calcular el siguiente mes de pago
            mes_siguiente = fecha_pago.month + 1 if fecha_pago.month < 12 else 1
            anio_siguiente = fecha_pago.year if mes_siguiente > 1 else fecha_pago.year + 1

            try:
                fecha_pago = date(anio_siguiente, mes_siguiente, self.fecha_inicio.day)
            except ValueError:
                _, last_day = monthrange(anio_siguiente, mes_siguiente)
                fecha_pago = date(anio_siguiente, mes_siguiente, last_day)

        # Restar pagos realizados
        pagos_realizados = self.pago_set.aggregate(models.Sum('monto_pagado'))['monto_pagado__sum'] or 0
        deuda_total -= float(pagos_realizados)

        return max(deuda_total, 0)  # Evitar valores negativos

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
