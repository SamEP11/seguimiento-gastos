from django.test import TestCase
from django.contrib.auth.models import User
from .models import Transaction, Category
from django.urls import reverse
from decimal import Decimal

# --- PRUEBAS DEL DASHBOARD (EXISTENTES, SIN CAMBIOS) ---
class DashboardViewTestCase(TestCase):
    """
    Pruebas para la vista del Dashboard.
    """
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.category1 = Category.objects.create(user=self.user1, name='Salario User1')
        Transaction.objects.create(user=self.user1, type='Ingreso', amount=500, category=self.category1, date='2025-07-03')

        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.category2 = Category.objects.create(user=self.user2, name='Comida User2')
        Transaction.objects.create(user=self.user2, type='Gasto', amount=50, category=self.category2, date='2025-07-03')

    def test_user_can_only_see_their_own_transactions(self):
        self.client.login(username='user2', password='password123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '50,00') 
        self.assertNotContains(response, '500,00')

    def test_dashboard_is_protected(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/dashboard/')


# --- PRUEBAS CRUD DE CATEGORÍAS (EXISTENTES, SIN CAMBIOS) ---
class CategoryCRUDTestCase(TestCase):
    """
    Pruebas para la creación, actualización y eliminación de categorías.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_create_category(self):
        initial_category_count = Category.objects.count()
        response = self.client.post(reverse('manage_categories'), {'name': 'Inversiones'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('manage_categories'))
        self.assertEqual(Category.objects.count(), initial_category_count + 1)
        self.assertTrue(Category.objects.filter(name='Inversiones').exists())

    def test_update_category(self):
        category = Category.objects.create(user=self.user, name='Ocio')
        response = self.client.post(reverse('update_category', args=[category.pk]), {'name': 'Tiempo Libre'})
        self.assertEqual(response.status_code, 302)
        category.refresh_from_db()
        self.assertEqual(category.name, 'Tiempo Libre')

    def test_delete_category(self):
        category = Category.objects.create(user=self.user, name='Temporal')
        initial_category_count = Category.objects.count()
        response = self.client.post(reverse('delete_category', args=[category.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Category.objects.count(), initial_category_count - 1)
        self.assertFalse(Category.objects.filter(pk=category.pk).exists())

    def test_user_cannot_edit_other_users_category(self):
        other_user = User.objects.create_user(username='otheruser', password='password123')
        other_category = Category.objects.create(user=other_user, name='Categoría Ajena')
        response = self.client.get(reverse('update_category', args=[other_category.pk]))
        self.assertEqual(response.status_code, 404)


# =================================================================
# NUEVAS PRUEBAS PARA EL CRUD DE TRANSACCIONES
# =================================================================
class TransactionCRUDTestCase(TestCase):
    """
    Pruebas para la creación, actualización y eliminación de transacciones.
    """
    def setUp(self):
        # Creamos un usuario y una categoría para usar en las pruebas
        self.user = User.objects.create_user(username='transactionuser', password='password123')
        self.category = Category.objects.create(user=self.user, name='Pruebas')
        self.client.login(username='transactionuser', password='password123')

    def test_create_transaction(self):
        """Prueba que un usuario puede crear una nueva transacción."""
        initial_transaction_count = Transaction.objects.count()
        
        transaction_data = {
            'amount': '150.75',
            'type': 'Ingreso',
            'category': self.category.pk,
            'date': '2025-07-10',
            'description': 'Ingreso de prueba'
        }
        
        response = self.client.post(reverse('add_transaction'), transaction_data)
        
        self.assertEqual(response.status_code, 302) # Esperamos una redirección
        self.assertEqual(Transaction.objects.count(), initial_transaction_count + 1)
        
        new_transaction = Transaction.objects.latest('created_at')
        self.assertEqual(new_transaction.amount, Decimal('150.75'))

    def test_update_transaction(self):
        """Prueba que un usuario puede actualizar una transacción existente."""
        transaction = Transaction.objects.create(
            user=self.user,
            amount='100.00',
            type='Gasto',
            category=self.category,
            date='2025-07-11'
        )
        
        update_data = {
            'amount': '125.50',
            'type': 'Gasto',
            'category': self.category.pk,
            'date': '2025-07-11',
            'description': 'Gasto actualizado'
        }
        
        response = self.client.post(reverse('update_transaction', args=[transaction.pk]), update_data)
        
        self.assertEqual(response.status_code, 302)
        
        transaction.refresh_from_db()
        self.assertEqual(transaction.amount, Decimal('125.50'))
        self.assertEqual(transaction.description, 'Gasto actualizado')

    def test_delete_transaction(self):
        """Prueba que un usuario puede eliminar una transacción."""
        transaction = Transaction.objects.create(
            user=self.user,
            amount='200.00',
            type='Ingreso',
            category=self.category,
            date='2025-07-12'
        )
        initial_transaction_count = Transaction.objects.count()
        
        response = self.client.post(reverse('delete_transaction', args=[transaction.pk]))
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Transaction.objects.count(), initial_transaction_count - 1)

    def test_user_cannot_delete_other_users_transaction(self):
        """Prueba que un usuario no puede eliminar la transacción de otro."""
        other_user = User.objects.create_user(username='otheruser2', password='password123')
        other_transaction = Transaction.objects.create(
            user=other_user,
            amount='999.00',
            type='Gasto',
            date='2025-07-13'
        )
        
        # Intentamos acceder a la página de borrado de la transacción ajena
        response = self.client.get(reverse('delete_transaction', args=[other_transaction.pk]))
        
        # Esperamos un error 404 (No Encontrado)
        self.assertEqual(response.status_code, 404)
