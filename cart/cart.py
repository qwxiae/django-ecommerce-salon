from django.conf import settings
from main.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    
    def add(self, product, seller, quantity=1):
        item_id = str(product.id)
        if item_id not in self.cart:
            self.cart[item_id] = {"quantity": 0, "seller": seller}
        self.cart[item_id]["quantity"] = quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        item_id = str(product.id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def get_total_price(self):
        total = 0
        for item_id, item_date in self.cart.items():
            try:
                product = Product.objects.get(id=item_id)
                total += product.current_price * item_date["quantity"]
            except Product.DoesNotExist:
                continue
        return total

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def __iter__(self):
        item_ids = self.cart.keys()
        items = Product.objects.filter(id__in=item_ids)
        for item in items:
            total_price = item.current_price
            quantity = self.cart[str(item.id)]["quantity"]
            seller = self.cart[str(item.id)]["seller"]
            yield {
                "item": item,
                "quantity": quantity,
                "seller": seller,
                "total_price": total_price * quantity,
                "current_price": total_price,
            }

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())
