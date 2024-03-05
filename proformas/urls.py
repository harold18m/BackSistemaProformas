from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import CrearProforma, PendientesProformas,HistorialProformas, HistorialProformasDetalle, tipo_de_cambio_view, imprimir_ultima_proforma, imprimir_proforma

urlpatterns = [
    path('api/crear-proforma/', CrearProforma.as_view(), name='crear_proforma'),
    path('api/historial-proformas/', HistorialProformas.as_view(), name='historial_proformas'),
    path('api/historial-proformas/<int:pk>/', HistorialProformasDetalle.as_view(), name='historial_proformas_detalle'),
    path('api/proformas-pendientes/', PendientesProformas.as_view() , name='proformas-pendientes'),
    path('api/tipo-de-cambio/', tipo_de_cambio_view),
    path('api/imprimir-proforma/<int:pk>/', imprimir_proforma, name='imprimir_proforma'),
    path('api/imprimir-ultima-proforma/', imprimir_ultima_proforma, name='imprimir_ultima_proforma'),
    path('api/token/', obtain_auth_token, name='obtain-token'),     
]