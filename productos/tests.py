from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Producto

VALIDO = {"nombre": "Teclado", "descripcion": "Mecánico", "precio": "100.50", "cantidad_disponible": "5"}


class ProductoTests(TestCase):
    def setUp(self):
        self.client.force_login(get_user_model().objects.create_user("ana", password="x"))

    def test_crear_valido(self):
        resp = self.client.post(reverse("productos:crear"), VALIDO)
        self.assertRedirects(resp, reverse("productos:lista"))
        self.assertEqual(Producto.objects.count(), 1)

    def test_rechaza_datos_invalidos(self):
        casos = {
            "nombre corto": {**VALIDO, "nombre": "ab"},
            "nombre vacío": {**VALIDO, "nombre": ""},
            "precio cero": {**VALIDO, "precio": "0"},
            "precio negativo": {**VALIDO, "precio": "-5"},
            "cantidad negativa": {**VALIDO, "cantidad_disponible": "-1"},
            "cantidad decimal": {**VALIDO, "cantidad_disponible": "2.5"},
            "descripción larga": {**VALIDO, "descripcion": "x" * 501},
        }
        for nombre, datos in casos.items():
            with self.subTest(nombre):
                resp = self.client.post(reverse("productos:crear"), datos)
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(Producto.objects.count(), 0)

    def test_editar_y_eliminar(self):
        p = Producto.objects.create(nombre="Mouse", precio=10, cantidad_disponible=1)
        self.client.post(reverse("productos:editar", args=[p.pk]), {**VALIDO, "nombre": "Mouse Pro"})
        p.refresh_from_db()
        self.assertEqual(p.nombre, "Mouse Pro")
        self.assertEqual(self.client.get(reverse("productos:eliminar", args=[p.pk])).status_code, 200)
        self.client.post(reverse("productos:eliminar", args=[p.pk]))
        self.assertFalse(Producto.objects.exists())

    def test_busqueda_por_nombre(self):
        Producto.objects.create(nombre="Teclado", precio=1, cantidad_disponible=1)
        Producto.objects.create(nombre="Monitor", precio=1, cantidad_disponible=1)
        resp = self.client.get(reverse("productos:lista"), {"q": "tecl"})
        self.assertContains(resp, "Teclado")
        self.assertNotContains(resp, "Monitor")
