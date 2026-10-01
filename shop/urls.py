from django.urls import path
from shop.views import products, basket, basket_add, basket_delete

app_name = "products"

urlpatterns = [
    path('', products, name='index'),
    path('category/<int:category_id>', products, name="category"),
    path('basket', basket, name='basket'),
    path('basket-add/<int:product_id>', basket_add, name="basket_add"),
    path('basket-delete/<int:basket_id>', basket_delete, name="basket_delete"),
]