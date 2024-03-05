import requests 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse
from bs4 import BeautifulSoup
from escpos.printer import Usb
from .models import Proforma, ItemProforma
from .serializers import ProformaSerializer, ItemProformaSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q

class CrearProforma(APIView):
    def post(self, request, *args, **kwargs):

        importe_total = request.data.get('importeTotal')
        if importe_total == 0 or importe_total == "0.00" or importe_total is None:
            return Response({'message': 'Debe insertar datos a las filas para guardar la proforma'}, status=status.HTTP_400_BAD_REQUEST)
            
        cliente = request.data.get('cliente')
        direccion = request.data.get('direccion')
        proforma_items = request.data.get('proformaItems', [])

        # Crear la nueva proforma
        nueva_proforma = Proforma(cliente=cliente)
        nueva_proforma.direccion = direccion
        nueva_proforma.importe_total = importe_total
        nueva_proforma.save()

        # Crear los items de la proforma
        for item_data in proforma_items:
            importe = item_data.get('importe')
            precio_unitario = item_data.get('punit')
            if importe != "0" and importe is not None and importe != "" and precio_unitario is not None:
                ItemProforma.objects.create(
                    proforma=nueva_proforma,
                    descripcion=item_data.get('descripcion'),
                    cantidad=item_data.get('cantidad'),
                    precio_unitario=precio_unitario,
                    importe=importe
                )

        return Response({'message': 'Proforma creada exitosamente', 'numero_proforma': nueva_proforma.numero_proforma}, status=status.HTTP_201_CREATED)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class HistorialProformas(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        numero_proforma = request.query_params.get('numero_proforma', None)
        if numero_proforma is not None:
            proformas = Proforma.objects.filter(numero_proforma__icontains=numero_proforma).order_by('-fecha', '-hora')
        else:
            proformas = Proforma.objects.all().order_by('-fecha', '-hora')
        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(proformas, request)
        serializer = ProformaSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class HistorialProformasDetalle(APIView):
    def get(self, request, *args, **kwargs):
        proforma = Proforma.objects.get(pk=kwargs['pk'])
        items = ItemProforma.objects.filter(proforma=proforma)
        serializer = ItemProformaSerializer(items, many=True)
        return Response(serializer.data)


def obtener_tipo_de_cambio():
    url = "https://www.google.com/finance/quote/USD-PEN?sa=X&ved=2ahUKEwiJ9_Pz3N7zAhXpIbkGHQsID6IQ3ecFegQINhAX"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    tipo_de_cambio = soup.find('div', class_='YMlKec fxKbKc').text
    return tipo_de_cambio

def tipo_de_cambio_view(request):
    tipo_de_cambio = obtener_tipo_de_cambio()
    return JsonResponse({'tipo_de_cambio': tipo_de_cambio})

def imprimir_ultima_proforma(request):
    try:
        proforma = Proforma.objects.order_by('-fecha', '-hora').first()
        if proforma is None:
            return JsonResponse({'status': 'error', 'message': 'No hay proformas para imprimir'})
        
        items = ItemProforma.objects.filter(proforma=proforma)
        item_serializer = ItemProformaSerializer(items, many=True)
        
        data = {
            'numero_proforma': proforma.numero_proforma,
            'cliente': proforma.cliente,
            'direccion': proforma.direccion,
            'fecha': proforma.fecha,
            'hora': proforma.hora.strftime("%H:%M"), 
            'proforma_items': item_serializer.data,
            'importe_total': proforma.importe_total,
        }
        
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def imprimir_proforma(request, pk):
    try:
        proforma = Proforma.objects.get(pk=pk)
        if proforma is None:
            return JsonResponse({'status': 'error', 'message': 'No hay proformas para imprimir'})
        
        items = ItemProforma.objects.filter(proforma=proforma)
        item_serializer = ItemProformaSerializer(items, many=True)
        
        data = {
            'numero_proforma': proforma.numero_proforma,
            'cliente': proforma.cliente,
            'direccion': proforma.direccion,
            'fecha': proforma.fecha,
            'hora': proforma.hora.strftime("%H:%M"), 
            'proforma_items': item_serializer.data,
            'importe_total': proforma.importe_total,
        }
        
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
from datetime import datetime

class PendientesProformas(APIView):

    def get(self, request, *args, **kwargs):
        today = datetime.now().date()
        proformas = Proforma.objects.filter(Q(fecha=today) | Q(completed=False)).order_by('fecha', 'hora')
        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(proformas, request)
        serializer = ProformaSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        proforma = Proforma.objects.get(pk=request.data.get('id'))
        proforma.completed = True
        proforma.save()
        return Response({'message': 'Proforma completada exitosamente'}, status=status.HTTP_200_OK)