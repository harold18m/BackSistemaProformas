from rest_framework import serializers
from .models import Proforma, ItemProforma

class ItemProformaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemProforma
        fields = ['descripcion', 'cantidad', 'precio_unitario', 'importe']

class ProformaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proforma
        fields = ['id' , 'numero_proforma','cliente','direccion','fecha', 'hora', 'importe_total', 'completed']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['hora'] = instance.hora.strftime("%H:%M")
        return representation
