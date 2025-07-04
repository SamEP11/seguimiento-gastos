from django.test import TestCase
from django.contrib.auth.models import User
from .models import Transaction, Category
from django.urls import reverse

class DashboardViewTestCase(TestCase):
    """
    Pruebas para la vista del Dashboard.
    """

    def setUp(self):
        """
        Esta función se ejecuta antes de cada prueba.
        Configuramos dos usuarios y algunas transacciones.
        """
        # Creamos Usuario 1
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.category1 = Category.objects.create(user=self.user1, name='Salario User1')
        self.transaction1 = Transaction.objects.create(
            user=self.user1,
            type='Ingreso',
            amount=500,
            category=self.category1,
            date='2025-07-03'
        )

        # Creamos Usuario 2
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.category2 = Category.objects.create(user=self.user2, name='Comida User2')
        self.transaction2 = Transaction.objects.create(
            user=self.user2,
            type='Gasto',
            amount=50,
            category=self.category2,
            date='2025-07-03'
        )

    def test_user_can_only_see_their_own_transactions(self):
        """
        Prueba que un usuario autenticado solo ve sus propias transacciones en el dashboard.
        """
        # Iniciamos sesión como Usuario 2
        self.client.login(username='user2', password='password123')

        # Accedemos a la URL del dashboard
        response = self.client.get(reverse('dashboard'))

        # 1. Verificamos que la petición fue exitosa (código 200)
        self.assertEqual(response.status_code, 200)

        # 2. Verificamos que la transacción del Usuario 2 ESTÁ en la página
        # CORRECCIÓN: Usamos la coma como separador decimal, como lo hace Django en español.
        self.assertContains(response, '50,00') 

        # 3. Verificamos que la transacción del Usuario 1 NO ESTÁ en la página
        self.assertNotContains(response, '500,00')

    def test_dashboard_is_protected(self):
        """
        Prueba que un usuario no autenticado no puede acceder al dashboard.
        """
        # No iniciamos sesión. Intentamos acceder al dashboard.
        response = self.client.get(reverse('dashboard'))

        # Verificamos que somos redirigidos a la página de login (código 302)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/dashboard/')

