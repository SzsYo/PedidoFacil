from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Pedido(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        CONFIRMADO = "confirmado", "Confirmado"
        CANCELADO = "cancelado", "Cancelado"

    numero_pedido = models.CharField("número de pedido", max_length=30, unique=True)
    cliente = models.CharField("cliente", max_length=120)
    fecha_registro = models.DateTimeField("fecha de registro", auto_now_add=True)
    descripcion = models.TextField("descripción", max_length=500)
    valor_total = models.DecimalField(
        "valor total",
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01, "El valor total debe ser mayor que cero.")],
    )
    estado = models.CharField(
        "estado", max_length=12, choices=Estado.choices, default=Estado.PENDIENTE
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="pedidos",
        verbose_name="registrado por",
    )

    class Meta:
        ordering = ["-fecha_registro"]
        verbose_name = "pedido"
        verbose_name_plural = "pedidos"
        constraints = [
            models.CheckConstraint(condition=models.Q(valor_total__gt=0), name="pedido_valor_mayor_cero"),
            models.CheckConstraint(
                condition=models.Q(estado__in=["pendiente", "confirmado", "cancelado"]),
                name="pedido_estado_valido",
            ),
        ]

    def __str__(self):
        return f"Pedido {self.numero_pedido} - {self.cliente}"
