from django.db import models
from bson.decimal128 import Decimal128
from decimal import Decimal

class Decimal128Field(models.DecimalField):
    def from_db_value(self, value, expression, connection):
        if isinstance(value, Decimal128):
            return value.to_decimal()
        return value

    def get_prep_value(self, value):
        if isinstance(value, Decimal):
            return Decimal128(value)
        return value

    def to_python(self, value):
        if isinstance(value, Decimal128):
            return value.to_decimal()
        if isinstance(value, str):
            return Decimal(value)
        return value


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=10)
    address = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=255, default='General')
    price = Decimal128Field(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class SaleOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    quantity = models.PositiveIntegerField()
    total_amount = Decimal128Field(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('COMPLETED', 'Completed'),
            ('CANCELLED', 'Cancelled'),
        ],
        default='PENDING',
    )

    def __str__(self):
        return f"Sale Order - {self.product.name} - {self.status}"

    def save(self, *args, **kwargs):
        if not self.total_amount:
            self.total_amount = Decimal(self.product.price) * Decimal(self.quantity)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Sale Order"
        verbose_name_plural = "Sale Orders"


class StockMovement(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    quantity = models.PositiveIntegerField()
    movement_type = models.CharField(max_length=50, choices=[('IN', 'In'), ('OUT', 'Out')])
    movement_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.product.name} - {self.movement_type}"

    def save(self, *args, **kwargs):
        self.quantity = int(self.quantity)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Stock Movement"
        verbose_name_plural = "Stock Movements"