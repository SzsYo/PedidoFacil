from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AutenticacionTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("ana", password="Clave-segura-123")

    def test_paginas_protegidas_redirigen_al_login(self):
        for nombre in ["productos:lista", "pedidos:lista", "productos:crear", "pedidos:crear"]:
            resp = self.client.get(reverse(nombre))
            self.assertEqual(resp.status_code, 302)
            self.assertIn(reverse("login"), resp.url)

    def test_login_correcto(self):
        resp = self.client.post(reverse("login"), {"username": "ana", "password": "Clave-segura-123"})
        self.assertRedirects(resp, reverse("productos:lista"), fetch_redirect_response=False)

    def test_login_incorrecto_muestra_mensaje(self):
        resp = self.client.post(reverse("login"), {"username": "ana", "password": "mala"})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Usuario o contraseña incorrectos")

    def test_logout(self):
        self.client.force_login(self.user)
        resp = self.client.post(reverse("logout"))
        self.assertRedirects(resp, reverse("login"), fetch_redirect_response=False)
        self.assertEqual(self.client.get(reverse("productos:lista")).status_code, 302)

    def test_password_no_se_guarda_en_texto_plano(self):
        self.assertNotEqual(self.user.password, "Clave-segura-123")
        self.assertTrue(self.user.password.startswith(("pbkdf2_", "argon2", "scrypt")))
