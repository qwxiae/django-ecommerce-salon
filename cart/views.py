from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from django.views import View
from main.models import Product, ProductSeller, Seller


def cart_detail(request):
    """Pass cart object to the html page"""
    cart = Cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart})


def cart_add(request, item_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=item_id)
    seller = request.POST.get('seller')

    if seller:
        try:
            seller_obj = Seller.objects.get(name=seller)
            product_seller = ProductSeller.objects.get(
                product=product,
                seller=seller_obj
            )
        except Seller.DoesNotExist:
            print('seller does not exist')
            return redirect('cart:cart_detail')
        except ProductSeller.DoesNotExist:
            print('product does not exist')
            return redirect('cart:cart_detail')
    else:
        # if seller is gone replace him 
        # available_sellers = product.seller
        available_sellers = ProductSeller.objects.filter(
            product=product)
        if available_sellers.exists():
            seller_obj = available_sellers.first().seller
            seller = seller_obj.name
        else:
            return redirect('cart:cart_detail')
    
    cart.add(product, seller)
    return redirect('cart:cart_detail')


def cart_remove(request, item_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=item_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


class CartUpdateView(View):
    def post(self, request, item_id):
        cart = Cart(request)
        quantity = request.POST.get("quantity", 1)
        try:
            quantity = int(quantity)
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1
        prodcut = get_object_or_404(Product, id=item_id)

        if quantity > 0:
            cart.add(prodcut, cart.cart[str(item_id)]['seller'], quantity)
        else:
            cart.remove(prodcut)

        return redirect('cart:cart_detail')