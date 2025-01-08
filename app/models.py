from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    dni = models.CharField(max_length=8)
    servicio = models.IntegerField(choices=[
        (25, '25'),
        (30, '30'),
        (35, '35'),
        (40, '40'),
        (50, '50')
    ])
    fecha_inicio = models.DateField()
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.nombre} {self.apellido_paterno} {self.apellido_materno}'

