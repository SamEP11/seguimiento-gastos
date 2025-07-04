
from django.contrib import admin
from .models import Category, Transaction

# Register your models here.



admin.site.register(Category)


# --- Registrando el modelo Transaction con más personalización ---
# Usamos una clase que hereda de ModelAdmin para personalizar cómo se muestra el modelo.

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Personalización del panel de administración para el modelo Transaction.
    """
    # Muestra estos campos en la lista de transacciones.
    list_display = ('user', 'type', 'amount', 'category', 'date')
    
    # Añade filtros en la barra lateral derecha para facilitar la búsqueda.
    list_filter = ('type', 'date', 'user')
    
    # Añade un campo de búsqueda para encontrar transacciones por su descripción.
    search_fields = ('description', 'category__name')

