from django.urls import path

from . import views

app_name = "pedidos"

urlpatterns = [
    path("", views.PedidoLista.as_view(), name="lista"),
    path("nuevo/", views.PedidoCrear.as_view(), name="crear"),
    path("<int:pk>/", views.PedidoDetalle.as_view(), name="detalle"),
    path("<int:pk>/editar/", views.PedidoEditar.as_view(), name="editar"),
    path("<int:pk>/eliminar/", views.PedidoEliminar.as_view(), name="eliminar"),
    path("<int:pk>/estado/", views.PedidoCambiarEstado.as_view(), name="cambiar_estado"),
]
