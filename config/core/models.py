from django.db import models
from django.contrib.auth.models import User

# --- Modelo para las Categorías de Gastos/Ingresos ---
# Cada usuario tendrá sus propias categorías.

class Category(models.Model):
    """
    Representa una categoría para una transacción, como "Comida", "Transporte", "Salario", etc.
    Cada categoría pertenece a un usuario específico.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ('user', 'name')


# --- Modelo para las Transacciones ---
# Aquí se registrarán todos los movimientos de dinero.

class Transaction(models.Model):
    """
    Representa una transacción individual, que puede ser un ingreso o un gasto.
    """
    TRANSACTION_TYPE_CHOICES = (
        ('Gasto', 'Gasto'),
        ('Ingreso', 'Ingreso'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)
    date = models.DateField()
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} de {self.amount} en {self.category.name if self.category else 'Sin Categoría'}"

    class Meta:
        # Ordena las transacciones por fecha, de la más reciente a la más antigua, por defecto.
        ordering = ['-date']
        verbose_name = "Transacción"
        verbose_name_plural = "Transacciones"
