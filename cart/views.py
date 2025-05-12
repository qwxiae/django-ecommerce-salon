from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from django.views import View
from main.models import Procedure, ProcedureSpecialist, Specialist


def cart_detail(request):
    """Pass cart object to the html page"""
    cart = Cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart})


def cart_add(request, item_id):
    cart = Cart(request)
    procedure = get_object_or_404(Procedure, id=item_id)
    specialist = request.POST.get('specialist')

    if specialist:
        try:
            specialist_obj = Specialist.objects.get(name=specialist)
            procedure_specialist = ProcedureSpecialist.objects.get(
                procedure=procedure,
                specialist=specialist_obj
            )
        except Specialist.DoesNotExist:
            print('specialist does not exist')
            return redirect('cart:cart_detail')
        except ProcedureSpecialist.DoesNotExist:
            print('procedure does not exist')
            return redirect('cart:cart_detail')
    else:
        # if specialist is gone replace him 
        # available_specialists = procedure.specialist
        available_specialists = ProcedureSpecialist.objects.filter(
            procedure=procedure)
        if available_specialists.exists():
            specialist_obj = available_specialists.first().specialist
            specialist = specialist_obj.name
        else:
            return redirect('cart:cart_detail')
    
    cart.add(procedure, specialist)
    return redirect('cart:cart_detail')


def cart_remove(request, item_id):
    cart = Cart(request)
    procedure = get_object_or_404(Procedure, id=item_id)
    cart.remove(procedure)
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
        prodcut = get_object_or_404(Procedure, id=item_id)

        if quantity > 0:
            cart.add(prodcut, cart.cart[str(item_id)]['specialist'], quantity)
        else:
            cart.remove(prodcut)

        return redirect('cart:cart_detail')