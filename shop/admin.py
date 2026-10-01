from django.contrib import admin

from shop.models import Product, ProductCategory, Basket


admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Basket)