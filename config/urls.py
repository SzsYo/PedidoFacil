from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("cuentas.urls")),
    path("productos/", include("productos.urls")),
    path("pedidos/", include("pedidos.urls")),
]
