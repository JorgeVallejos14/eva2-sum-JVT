from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=120)
    telefono = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    direccion = models.CharField(max_length=200)
    saldo = models.DecimalField(max_digits=12, decimal_places=0, default=0)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Atencion(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='atenciones',
    )
    titulo = models.CharField(max_length=150)
    fecha = models.DateField()
    descripcion = models.TextField()
    monto = models.DecimalField(max_digits=12, decimal_places=0)

    class Meta:
        ordering = ['-fecha', 'titulo']
        verbose_name = 'atención'
        verbose_name_plural = 'atenciones'

    def __str__(self):
        return f'{self.titulo} - {self.cliente.nombre}'
