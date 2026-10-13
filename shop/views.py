from django.shortcuts import render, HttpResponseRedirect
from shop.models import Product, ProductCategory, Basket, Favorite
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
        'category_id': category_id,
    }

    if category_id:
        filtered_products = Product.objects.filter(category_id=category_id)
    else:
        filtered_products = Product.objects.all()

    search_query = request.GET.get('search', '')
    if search_query:
        filtered_products = filtered_products.filter(name__icontains=search_query)
    context['search_query'] = search_query

    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    if price_min:
        filtered_products = filtered_products.filter(price__gte=price_min)
    if price_max:
        filtered_products = filtered_products.filter(price__lte=price_max)
    context['price_min'] = price_min
    context['price_max'] = price_max

    sort = request.GET.get('sort', '')
    if sort == 'price_asc':
        filtered_products = filtered_products.order_by('price')
    elif sort == 'price_desc':
        filtered_products = filtered_products.order_by('-price')
    elif sort == 'name_asc':
        filtered_products = filtered_products.order_by('name')
    elif sort == 'newest':
        filtered_products = filtered_products.order_by('-id')
    context['current_sort'] = sort

    paginator = Paginator(filtered_products, 6)
    page = request.GET.get('page', page)
    products_paginator = paginator.page(page)

    context.update({
        'products': products_paginator,
    })

    if request.user.is_authenticated:
        favorite_ids = list(Favorite.objects.filter(user=request.user).values_list('product_id', flat=True))
    else:
        favorite_ids = []
    context['favorite_ids'] = favorite_ids

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

@login_required
def favorites(request):
    favorites_list = Favorite.objects.filter(user=request.user).order_by('-created_timestamp')

    context = {
        'favorites': favorites_list,
        'title': 'Избранное',
    }
    return render(request, 'shop/favorites.html', context)


@login_required
def favorite_add(request, product_id):
    product = Product.objects.get(id=product_id)
    Favorite.objects.get_or_create(user=request.user, product=product)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def favorite_delete(request, product_id):
    Favorite.objects.filter(user=request.user, product_id=product_id).delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))



