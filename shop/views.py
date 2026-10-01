from django.shortcuts import render, HttpResponseRedirect
from shop.models import Product, ProductCategory, Basket
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def index(request):
    context = {
        "title": "четыре опоры",
        'categories': ProductCategory.objects.all(),
    }
    return render(request, "shop/index.html", context)


def products(request, category_id=None, page=1):
    context = {
        'title': 'каталог',
        'categories': ProductCategory.objects.all(),
    }

    if category_id:
        context.update({
            "products": Product.objects.filter(category_id=category_id)
        })
    else:
        context.update({
            "products": Product.objects.all()
        })

    return render(request, 'shop/products.html', context)


@login_required
def basket(request):
    baskets = Basket.objects.filter(user=request.user)

    total_quantity = sum(b.quantity for b in baskets)
    total_sum = sum(b.sum() for b in baskets)

    context = {
        'baskets': baskets,
        'total_quantity': total_quantity,
        'total_sum': total_sum,
        'title': 'Корзина',
    }
    return render(request, 'shop/basket.html', context)

@login_required
def basket_add(request, product_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('users:login'))

    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def basket_delete(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))



