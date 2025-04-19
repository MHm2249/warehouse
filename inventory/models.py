from django.db import models
from django.core.exceptions import ValidationError  # This was missing

class Product(models.Model):
    name = models.CharField(max_length=100)
    barcode = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)  # Add this field
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    restock_level = models.PositiveIntegerField(default=10)  # Optional: for inventory alerts
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # Optional

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
class Warehouse(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='warehouse')  # Changed to OneToOne
    stock = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.stock} units"
        
    def save(self, *args, **kwargs):
        if self.stock < 0:
            raise ValidationError("Stock cannot be negative")
        super().save(*args, **kwargs)

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    )
    
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='transactions')  # Changed to PROTECT
    quantity = models.PositiveIntegerField()  # Changed to PositiveInteger
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    notes = models.TextField(blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.product.name}"
        
    def clean(self):
        if self.transaction_type == 'OUT':
            warehouse = self.product.warehouse  # Using the related_name
            if self.quantity > warehouse.stock:
                raise ValidationError(
                    f"Not enough stock! Available: {warehouse.stock}, Requested: {self.quantity}"
                )
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Ensures clean() is called before save
        super().save(*args, **kwargs)