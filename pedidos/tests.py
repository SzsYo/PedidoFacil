from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Pedido

VALIDO = {
    "numero_pedido": "PED-1",
    "cliente": "María",
    "descripcion": "2 teclados",
    "valor_total": "300000",
    "estado": "pendiente",
}


class PedidoTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("ana", password="x")
        self.client.force_login(self.user)

    def test_crear_asocia_usuario_autenticado(self):
        self.client.post(reverse("pedidos:crear"), VALIDO)
        self.assertEqual(Pedido.objects.get().usuario, self.user)

    def test_numero_duplicado_rechazado(self):
        self.client.post(reverse("pedidos:crear"), VALIDO)
        resp = self.client.post(reverse("pedidos:crear"), {**VALIDO, "cliente": "Otro"})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Ya existe un pedido con este número")
        self.assertEqual(Pedido.objects.count(), 1)

    def test_rechaza_datos_invalidos(self):
        casos = {
            "estado inválido": {**VALIDO, "estado": "enviado"},
            "valor cero": {**VALIDO, "valor_total": "0"},
            "valor negativo": {**VALIDO, "valor_total": "-1"},
            "cliente vacío": {**VALIDO, "cliente": ""},
            "número vacío": {**VALIDO, "numero_pedido": ""},
            "descripción vacía": {**VALIDO, "descripcion": ""},
        }
        for nombre, datos in casos.items():
            with self.subTest(nombre):
                resp = self.client.post(reverse("pedidos:crear"), datos)
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(Pedido.objects.count(), 0)

    def test_editar_permite_conservar_su_numero(self):
        p = Pedido.objects.create(**{**VALIDO, "valor_total": 5}, usuario=self.user)
        resp = self.client.post(reverse("pedidos:editar", args=[p.pk]), {**VALIDO, "cliente": "Nuevo"})
        self.assertRedirects(resp, reverse("pedidos:lista"))
        p.refresh_from_db()
        self.assertEqual(p.cliente, "Nuevo")

    def test_cambiar_estado(self):
        p = Pedido.objects.create(**{**VALIDO, "valor_total": 5}, usuario=self.user)
        self.client.post(reverse("pedidos:cambiar_estado", args=[p.pk]), {"estado": "confirmado"})
        p.refresh_from_db()
        self.assertEqual(p.estado, "confirmado")
        self.client.post(reverse("pedidos:cambiar_estado", args=[p.pk]), {"estado": "xxx"})
        p.refresh_from_db()
        self.assertEqual(p.estado, "confirmado")

    def test_eliminar_pendiente_si_confirmado_no(self):
        p = Pedido.objects.create(**{**VALIDO, "valor_total": 5}, usuario=self.user)
        self.client.post(reverse("pedidos:eliminar", args=[p.pk]))
        self.assertFalse(Pedido.objects.exists())
        c = Pedido.objects.create(**{**VALIDO, "valor_total": 5, "estado": "confirmado"}, usuario=self.user)
        self.client.post(reverse("pedidos:eliminar", args=[c.pk]))
        self.assertTrue(Pedido.objects.filter(pk=c.pk).exists())

    def test_busqueda_por_cliente(self):
        Pedido.objects.create(**{**VALIDO, "valor_total": 5}, usuario=self.user)
        resp = self.client.get(reverse("pedidos:lista"), {"q": "mar"})
        self.assertContains(resp, "PED-1")
        resp = self.client.get(reverse("pedidos:lista"), {"q": "zzz"})
        self.assertNotContains(resp, "PED-1")
