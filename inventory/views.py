from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Supplier, SaleOrder, StockMovement
from .forms import ProductForm, SupplierForm, SaleOrderForm, StockMovementForm
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_products')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

def list_products(request):
    products = Product.objects.all()
    return render(request, 'list_products.html', {'products': products})

def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            print("Form is valid. Saving supplier...")
            form.save()
            return redirect('list_suppliers')
        else:
            print("Form errors:", form.errors) 
    else:
        form = SupplierForm()
    return render(request, 'add_supplier.html', {'form': form})

def list_suppliers(request):
    suppliers = Supplier.objects.all()
    return render(request, 'list_suppliers.html', {'suppliers': suppliers})


def stock_movement(request):
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            movement_type = form.cleaned_data['movement_type']
            quantity = form.cleaned_data['quantity']

            if movement_type == 'IN':
                product.stock_quantity += quantity
            else:
                product.stock_quantity -= quantity
                if product.stock_quantity < 0:
                    form.add_error('quantity', 'Stock cannot go negative.')
                    return render(request, 'stock_movement.html', {'form': form})
            product.save()
            form.save()
            return redirect('list_products')
    else:
        form = StockMovementForm()
    return render(request, 'stock_movement.html', {'form': form})


def create_sale_order(request):
    if request.method == 'POST':
        form = SaleOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_sale_orders')  
    else:
        form = SaleOrderForm()
    return render(request, 'create_sale_order.html', {'form': form})

def cancel_sale_order(request):

    sale_orders = SaleOrder.objects.filter(status='PENDING')
    if request.method == 'POST':
        order_id = request.POST.get('cancel_order')

        if order_id:
            try:
                order = SaleOrder.objects.get(id=order_id)

                if order.status == 'PENDING':
                    order.status = 'CANCELLED'
                    order.save()

                    product = order.product
                    product.stock_quantity += order.quantity
                    product.save()

                    StockMovement.objects.create(
                        product=product,
                        quantity=order.quantity,
                        movement_type='IN',
                    )
                    return redirect('cancel_sale_order') 

            except SaleOrder.DoesNotExist:
                return render(request, 'error.html', {'message': 'Sale order not found.'})

    return render(request, 'cancel_sale_order.html', {'sale_orders': sale_orders})

def fetch_pending_orders(request):
    if request.method == 'GET':
        pending_orders = SaleOrder.objects.filter(status='PENDING')
        return render(request, 'complete_sale_order.html', {'pending_orders': pending_orders})
    return HttpResponse("Invalid request method.", status=400)

def mark_order_complete(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(SaleOrder, id=order_id)

        if order.status == 'COMPLETED':
            pending_orders = SaleOrder.objects.filter(status='PENDING')
            return render(request, 'complete_sale_order.html', {'pending_orders': pending_orders})

        order.status = 'COMPLETED'
        order.save()
        pending_orders = SaleOrder.objects.filter(status='PENDING')
        return render(request, 'complete_sale_order.html', {'pending_orders': pending_orders})

    return HttpResponse("Invalid request method.", status=400)

def list_sale_orders(request):
    sale_orders = SaleOrder.objects.all().select_related('product')
    return render(request, 'list_sale_orders.html', {'sale_orders': sale_orders})

def check_stock_levels(request):
    products = Product.objects.all()
    stock_levels = []

    for product in products:
        current_stock = product.stock_quantity
        stock_levels.append({
            'product': product,
            'current_stock': current_stock
        })
    return render(request, 'stock_report.html', {'stock_levels': stock_levels})