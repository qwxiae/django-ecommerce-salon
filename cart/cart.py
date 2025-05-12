from django.conf import settings
from main.models import Procedure


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    
    def add(self, procedure, specialist, quantity=1):
        item_id = str(procedure.id)
        if item_id not in self.cart:
            self.cart[item_id] = {"quantity": 0, "specialist": specialist}
        self.cart[item_id]["quantity"] = quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, procedure):
        item_id = str(procedure.id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def get_total_price(self):
        total = 0
        for item_id, item_date in self.cart.items():
            try:
                procedure = Procedure.objects.get(id=item_id)
                total += procedure.current_price * item_date["quantity"]
            except Procedure.DoesNotExist:
                continue
        return total

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def __iter__(self):
        item_ids = self.cart.keys()
        items = Procedure.objects.filter(id__in=item_ids)
        for item in items:
            total_price = item.current_price
            quantity = self.cart[str(item.id)]["quantity"]
            specialist = self.cart[str(item.id)]["specialist"]
            yield {
                "item": item,
                "quantity": quantity,
                "specialist": specialist,
                "total_price": total_price * quantity,
                "current_price": total_price,
            }

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())
