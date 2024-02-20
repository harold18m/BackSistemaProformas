# En tu aplicación (por ejemplo, 'tu_app/filters.py')
import django_filters
from .models import Proforma

class ProformaFilter(django_filters.FilterSet):
    class Meta:
        model = Proforma
        fields = ['numero_proforma', 'cliente', 'importe_total']
