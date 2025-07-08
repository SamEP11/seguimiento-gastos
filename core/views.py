from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from datetime import datetime
import json
from django.contrib import messages
from django.db import IntegrityError

# --- Imports para la exportación a CSV ---
import csv
from django.http import HttpResponse


from .forms import RegistrationForm, TransactionForm, CategoryForm
from .models import Transaction, Category

# Vista de Registro (sin cambios)
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Category.objects.create(user=user, name='Comida')
            Category.objects.create(user=user, name='Transporte')
            Category.objects.create(user=user, name='Salario')
            login(request, user)
            return redirect('dashboard') 
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

# Vista del Dashboard (sin cambios)
@login_required
def dashboard(request):
    current_year = datetime.now().year
    current_month = datetime.now().month
    year = int(request.GET.get('year', current_year))
    month = int(request.GET.get('month', current_month))
    transactions = Transaction.objects.filter(user=request.user, date__year=year, date__month=month)
    total_income = transactions.filter(type='Ingreso').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = transactions.filter(type='Gasto').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expenses
    expenses_by_category = (transactions.filter(type='Gasto').values('category__name').annotate(total=Sum('amount')).order_by('-total'))
    chart_labels = [item['category__name'] for item in expenses_by_category]
    chart_data = [float(item['total']) for item in expenses_by_category]
    month_options = (Transaction.objects.filter(user=request.user).annotate(month=TruncMonth('date')).values('month').distinct().order_by('-month'))
    context = {
        'transactions': transactions.order_by('-date'),
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'month_options': month_options,
        'selected_year': year,
        'selected_month': month,
    }
    return render(request, 'dashboard.html', context)

# CRUD de Transacciones (sin cambios)
@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, '¡Transacción guardada con éxito!')
            return redirect('dashboard')
    else:
        form = TransactionForm(user=request.user)
    return render(request, 'add_transaction.html', {'form': form})

@login_required
def update_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Transacción actualizada con éxito!')
            return redirect('dashboard')
    else:
        form = TransactionForm(user=request.user, instance=transaction)
    return render(request, 'update_transaction.html', {'form': form, 'transaction': transaction})

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, '¡Transacción eliminada con éxito!')
        return redirect('dashboard')
    return render(request, 'delete_transaction.html', {'transaction': transaction})

# CRUD de Categorías (sin cambios)
@login_required
def manage_categories(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            try:
                category = form.save(commit=False)
                category.user = request.user
                category.save()
                messages.success(request, f"¡Categoría '{category.name}' creada con éxito!")
            except IntegrityError:
                messages.error(request, 'Ya existe una categoría con ese nombre.')
            return redirect('manage_categories') 
    else:
        form = CategoryForm()
    categories = Category.objects.filter(user=request.user).order_by('name')
    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'manage_categories.html', context)

@login_required
def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f"Categoría '{category.name}' actualizada con éxito.")
                return redirect('manage_categories')
            except IntegrityError:
                messages.error(request, 'Ya existe otra categoría con ese nombre.')
    else:
        form = CategoryForm(instance=category)
    categories = Category.objects.filter(user=request.user).order_by('name')
    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'manage_categories.html', context)

@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f"Categoría '{category_name}' eliminada con éxito.")
        return redirect('manage_categories')
    return render(request, 'delete_category.html', {'category': category})

# =================================================================
# NUEVA VISTA PARA EXPORTAR TRANSACCIONES A CSV
# =================================================================
@login_required
def export_transactions_csv(request):
    # 1. Crear la respuesta HTTP con las cabeceras CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_transacciones.csv"'

    # 2. Crear un "escritor" de CSV que escriba en la respuesta
    writer = csv.writer(response)

    # 3. Escribir la fila de encabezado
    writer.writerow(['Fecha', 'Tipo', 'Categoría', 'Monto', 'Descripción'])

    # 4. Obtener los parámetros de fecha del Dashboard
    year = request.GET.get('year', datetime.now().year)
    month = request.GET.get('month', datetime.now().month)

    # 5. Filtrar las transacciones del usuario para ese período
    transactions = Transaction.objects.filter(
        user=request.user, 
        date__year=year, 
        date__month=month
    ).order_by('date')

    # 6. Escribir cada transacción en una fila del CSV
    for transaction in transactions:
        writer.writerow([
            transaction.date,
            transaction.type,
            transaction.category.name if transaction.category else 'Sin Categoría',
            transaction.amount,
            transaction.description
        ])

    # 7. Devolver la respuesta al navegador
    return response
