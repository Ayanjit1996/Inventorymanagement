from django.contrib import admin
from django.urls import path
from .views import (
    home,
    add_product,
    list_products,
    add_supplier,
    list_suppliers,
    stock_movement,
    create_sale_order,
    cancel_sale_order,
    fetch_pending_orders,
    mark_order_complete,
    list_sale_orders,
    check_stock_levels,
)

urlpatterns = [
    path('', home, name='home'),
    path('add_product/', add_product, name='add_product'),
    path('list_products/', list_products, name='list_products'),
    path('add_supplier/', add_supplier, name='add_supplier'),
    path('list_suppliers/', list_suppliers, name='list_suppliers'),
    path('stock_movement/', stock_movement, name='stock_movement'),
    path('create_sale_order/', create_sale_order, name='create_sale_order'),
    path('cancel_sale_order/', cancel_sale_order, name='cancel_sale_order'),
    path('complete_sale_order/', fetch_pending_orders, name='fetch_pending_orders'),
    path('mark_order_complete/<int:order_id>/', mark_order_complete, name='mark_order_complete'),
    path('list_sale_orders/', list_sale_orders, name='list_sale_orders'),
    path('stock_report/', check_stock_levels, name='stock_report'),
]