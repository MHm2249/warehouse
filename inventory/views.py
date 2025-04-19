from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from .models import Product, Warehouse, Transaction
from .forms import ProductForm, TransactionForm
from django.http import JsonResponse
from .models import Warehouse

def stock_api(request, product_id):
    try:
        warehouse = Warehouse.objects.get(product_id=product_id)
        return JsonResponse({'stock': warehouse.stock})
    except Warehouse.DoesNotExist:
        return JsonResponse({'stock': 0})
    from django.views.generic import ListView


class TransactionListView(ListView):
    model = Transaction
    template_name = 'inventory/transaction_list.html'
    context_object_name = 'transactions'
    ordering = ['-transaction_date']

class ProductListView(ListView):
    model = Product
    template_name = 'inventory/product_list.html'
    context_object_name = 'products'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = '/products/'

from django.shortcuts import render
from django.contrib import messages

class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'inventory/transaction_form.html'
    success_url = '/'

    def form_valid(self, form):
        product = form.cleaned_data['product']
        quantity = form.cleaned_data['quantity']
        transaction_type = form.cleaned_data['transaction_type']
        
        warehouse, created = Warehouse.objects.get_or_create(product=product)
        
        if transaction_type == 'OUT' and quantity > warehouse.stock:
            messages.error(self.request, 
                         f"Not enough stock! Available: {warehouse.stock}, Requested: {quantity}")
            return self.form_invalid(form)
            
        # Proceed with transaction if validation passes
        transaction = form.save()
        
        # Update warehouse stock
        if transaction_type == 'IN':
            warehouse.stock += quantity
        else:
            warehouse.stock -= quantity
            
        warehouse.save()
        return super().form_valid(form)
from django.views.generic import ListView
from .models import Warehouse

class DashboardView(ListView):
    model = Warehouse
    template_name = 'inventory/dashboard.html'
    context_object_name = 'warehouse_items'
    
    def get_queryset(self):
        return Warehouse.objects.select_related('product').all()
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy

class ProductDetailView(DetailView):
    model = Product
    template_name = 'inventory/product_detail.html'
    context_object_name = 'product'

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm  # Use your existing ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('product-list')

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product

class ProductListView(ListView):
    model = Product
    template_name = 'inventory/product_list.html'
    context_object_name = 'products'







class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'inventory/product_confirm_delete.html'
    success_url = reverse_lazy('product-list')

from django import forms
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Product, Transaction, Warehouse
from .forms import TransactionForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# ... your existing views ...

def product_restock(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))
        if quantity > 0:
            product.quantity += quantity
            product.save()
            
            # Create a transaction record
            Transaction.objects.create(
                product=product,
                transaction_type='IN',
                quantity=quantity,
                notes=f"Manual restock - {request.POST.get('notes', '')}"
            )
            
            messages.success(request, f'Successfully restocked {quantity} units of {product.name}')
            return redirect('product-detail', pk=product.pk)
        else:
            messages.error(request, 'Quantity must be greater than zero')
    
    return render(request, 'inventory/product_restock.html', {
        'product': product,
        'current_stock': product.quantity,
    })