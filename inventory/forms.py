# forms.py
from django import forms
from .models import Product, Supplier, SaleOrder, StockMovement
from django.core.exceptions import ValidationError
import re

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'stock_quantity', 'supplier']
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['supplier'].queryset = Supplier.objects.all()

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price
    
    def clean_stock_quantity(self):
        stock_quantity = self.cleaned_data.get('stock_quantity')
        if stock_quantity < 0:
            raise forms.ValidationError("Stock quantity cannot be negative.")
        return stock_quantity

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Product.objects.filter(name=name).exists():
            raise forms.ValidationError("A product with this name already exists.")
        return name

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_email', 'contact_phone', 'address']
    
    def clean_contact_email(self):
        email = self.cleaned_data.get('contact_email')
        print(f"Validating email: {email}")
        if Supplier.objects.filter(contact_email=email).exists():
            raise ValidationError("A supplier with this email already exists.")
        return email

    def clean_contact_phone(self):
        phone = self.cleaned_data.get('contact_phone')
        print(f"Validating phone: {phone}")
        if not re.match(r'^\d{10}$', phone):
            raise ValidationError("Phone number must be exactly 10 digits.")
        
        if Supplier.objects.filter(contact_phone=phone).exists():
            raise ValidationError("A supplier with this phone number already exists.")
        
        return phone

    def clean_name(self):
        name = self.cleaned_data.get('name')
        print(f"Validating name: {name}")
        if Supplier.objects.filter(name=name).exists():
            raise ValidationError("A supplier with this name already exists.")
        return name

class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product', 'quantity', 'movement_type']

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        movement_type = self.cleaned_data.get('movement_type')
        product = self.cleaned_data.get('product')

        if movement_type == 'OUT' and product.stock_quantity < quantity:
            raise forms.ValidationError(f"Cannot move {quantity} units. Only {product.stock_quantity} units are available.")
        return quantity

class SaleOrderForm(forms.ModelForm):
    class Meta:
        model = SaleOrder
        fields = ['product', 'quantity']

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        product = self.cleaned_data.get('product')

        if quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")

        if product and quantity > product.stock_quantity:
            raise ValidationError(
                f"Not enough stock available for {product.name}. "
                f"Only {product.stock_quantity} units are available."
            )
        return quantity

    def save(self, commit=True):
        instance = super().save(commit=False)
        product = instance.product
        instance.total_amount = product.price * instance.quantity

        if commit:
            product.stock_quantity -= instance.quantity
            product.save()
            instance.save()

        return instance