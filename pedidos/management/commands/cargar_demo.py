from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from pedidos.models import Pedido
from productos.models import Producto

PRODUCTOS = [
    ("Teclado mecánico", "Teclado mecánico retroiluminado, layout español", "189900.00", 25),
    ("Mouse inalámbrico", "Mouse ergonómico con receptor USB", "54900.00", 60),
    ("Monitor 24 pulgadas", "Monitor Full HD con entrada HDMI", "649000.00", 12),
    ("Audífonos con micrófono", "Diadema USB para videollamadas", "89900.00", 40),
    ("Cable HDMI 2 m", "Cable HDMI 2.0 de alta velocidad", "18500.00", 150),
    ("Memoria USB 64 GB", "Memoria USB 3.0", "32000.00", 0),
]

PEDIDOS = [
    ("PED-0001", "María Gómez", "2 teclados mecánicos", "379800.00", "pendiente"),
    ("PED-0002", "Carlos Ramírez", "1 monitor y 1 cable HDMI", "667500.00", "confirmado"),
    ("PED-0003", "Laura Herrera", "3 mouse inalámbricos", "164700.00", "confirmado"),
    ("PED-0004", "Andrés Torres", "1 audífonos con micrófono", "89900.00", "cancelado"),
    ("PED-0005", "Sofía Martínez", "5 memorias USB y 2 cables HDMI", "197000.00", "pendiente"),
]


class Command(BaseCommand):
    help = "Carga productos y pedidos de ejemplo (usa el primer superusuario como responsable)."

    def handle(self, *args, **options):
        usuario = get_user_model().objects.filter(is_superuser=True).first()
        if usuario is None:
            raise CommandError("Primero crea un usuario con: python manage.py createsuperuser")

        for nombre, desc, precio, cant in PRODUCTOS:
            Producto.objects.get_or_create(
                nombre=nombre,
                defaults={"descripcion": desc, "precio": precio, "cantidad_disponible": cant},
            )
        for numero, cliente, desc, valor, estado in PEDIDOS:
            Pedido.objects.get_or_create(
                numero_pedido=numero,
                defaults={
                    "cliente": cliente,
                    "descripcion": desc,
                    "valor_total": valor,
                    "estado": estado,
                    "usuario": usuario,
                },
            )
        self.stdout.write(self.style.SUCCESS("Datos de ejemplo cargados."))
