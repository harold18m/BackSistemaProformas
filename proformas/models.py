from django.db import models
from django.db.models import Max

# Create your models here.
class Proforma(models.Model):
    numero_proforma = models.CharField(max_length=7, unique=True)
    cliente = models.CharField(max_length=50, null=True, blank=True)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    importe_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        fecha_formateada = self.fecha.strftime('%d/%m/%Y')
        return self.numero_proforma + ' / ' + self.cliente + ' / ' + fecha_formateada
    
    def save(self, *args, **kwargs):
        if not self.numero_proforma:
            max_numero = Proforma.objects.all().aggregate(Max('numero_proforma'))['numero_proforma__max']
            if max_numero is not None:
                self.numero_proforma = '{:07d}'.format(int(max_numero) + 1)
            else:
                self.numero_proforma = '0000001'
        super().save(*args, **kwargs)

class ItemProforma(models.Model):
    proforma = models.ForeignKey(Proforma, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=5)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    importe = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.descripcion
    