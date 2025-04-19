from django import forms
from .models import Product, Transaction

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'barcode', 'category']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['product', 'quantity', 'transaction_type', 'notes']