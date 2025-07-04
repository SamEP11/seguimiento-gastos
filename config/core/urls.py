# core/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transaction/add/', views.add_transaction, name='add_transaction'),
    path('transaction/<int:pk>/update/', views.update_transaction, name='update_transaction'),
    path('transaction/<int:pk>/delete/', views.delete_transaction, name='delete_transaction'),
    path('category/<int:pk>/update/', views.update_category, name='update_category'),
    path('category/<int:pk>/delete/', views.delete_category, name='delete_category'),
    path('categories/', views.manage_categories, name='manage_categories'),
]
