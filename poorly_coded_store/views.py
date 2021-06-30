from django.shortcuts import render, redirect
from .models import Order, Product

def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)


def checkout(request):
    if "quant" not in request.session:
        request.session["quant"]=0
    
    if "charge" not in request.session:
        request.session["charge"]=0

    quantity_from_form = int(request.POST["quantity"])          #q de productos de la compra actual
    idSelectedProduct=request.POST["price"]                     #traigo el id del producto que esta comprando
    selectedProduct=Product.objects.get(id=idSelectedProduct)   #recupero el obj producto para usar el precio   
    price_from_form = float(selectedProduct.price)              #guardo el precio en la variable
   
    total_charge_order = quantity_from_form * price_from_form   #calc la cant por el precio
    request.session['quant']+=quantity_from_form
    request.session["charge"]+=total_charge_order

    print(f"Charging credit card...{total_charge_order}")
    Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge_order) # se crea la orden
   
    ttlQtty= request.session['quant']
    ttlCharge=request.session["charge"]

    print(f"total:{ttlCharge}")  
    print(f"cant total:{ttlQtty}")
    
    return redirect(f"/checking_out/{ttlQtty}/{total_charge_order}/{ttlCharge}") #redirecciono para no producir doble cargo (del post)


def checkoutHtml(request, qty, ttl, ttlGrl):
    context = {
        "quantity":qty,
        "totalGrl":ttlGrl,
        "priceLastPurchase":ttl
    }
    return render(request, "store/checkout.html", context)