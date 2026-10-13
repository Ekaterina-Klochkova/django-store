from django.urls import path
from shop.views import products, basket, basket_add, basket_delete, favorites, favorite_add, favorite_delete

app_name = "products"

urlpatterns = [
    path('', products, name='index'),
    path('category/<int:category_id>', products, name="category"),
    path('page/<int:page>', products, name="page"),
    path('basket', basket, name='basket'),
    path('basket-add/<int:product_id>', basket_add, name="basket_add"),
    path('basket-delete/<int:basket_id>', basket_delete, name="basket_delete"),
    path('favorites/', favorites, name='favorites'),
    path('favorite-add/<int:product_id>', favorite_add, name="favorite_add"),
    path('favorite-delete/<int:product_id>', favorite_delete, name="favorite_delete"),
]