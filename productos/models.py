from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models


class Producto(models.Model):
    nombre = models.CharField(
        "nombre",
        max_length=100,
        validators=[MinLengthValidator(3, "El nombre debe tener al menos 3 caracteres.")],
    )
    descripcion = models.TextField("descripción", max_length=500, blank=True)
    precio = models.DecimalField(
        "precio",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01, "El precio debe ser mayor que cero.")],
    )
    cantidad_disponible = models.PositiveIntegerField(
        "cantidad disponible",
        validators=[MinValueValidator(0, "La cantidad no puede ser negativa.")],
    )
    fecha_registro = models.DateTimeField("fecha de registro", auto_now_add=True)

    class Meta:
        ordering = ["-fecha_registro"]
        verbose_name = "producto"
        verbose_name_plural = "productos"
        constraints = [
            models.CheckConstraint(condition=models.Q(precio__gt=0), name="producto_precio_mayor_cero"),
        ]

    def __str__(self):
        return self.nombre
