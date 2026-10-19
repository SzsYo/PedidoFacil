from django.urls import path

from . import views

app_name = "productos"

urlpatterns = [
    path("", views.ProductoLista.as_view(), name="lista"),
    path("nuevo/", views.ProductoCrear.as_view(), name="crear"),
    path("<int:pk>/", views.ProductoDetalle.as_view(), name="detalle"),
    path("<int:pk>/editar/", views.ProductoEditar.as_view(), name="editar"),
    path("<int:pk>/eliminar/", views.ProductoEliminar.as_view(), name="eliminar"),
]
