from itertools import product
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from strore.models import Cart, Order, Product

# Create your views here.
def index(request):

    products = Product.objects.all()
    return render(request,'store/index.html', context= {"produits" : products});

def product_detail(request, slug):
   product = get_object_or_404(Product, slug=slug)
   return render(request,'store/detail.html',context={"produitDetail" : product});

def add_to_cart(request,slug):
    user = request.user
    product = get_object_or_404(Product,  slug=slug)
    cart, _ = Cart.objects.get_or_create(user = user)
    order, create = Order.objects.get_or_create(user = user ,
                                                    ordered = False,
                                                    product = product)
    
    if create:
        cart.order.add(order)
        cart.save()
    
    else:
        order.quantity +=1
        order.save()

    return redirect(reverse("product", kwargs={"slug" : slug}))

def cart (request):
    cart = get_object_or_404(Cart, user =request.user)
    return render(request, 'store/cart.html', context={"order": cart.order.all()})

def delete_cart(request):
    #cart:=request.cart.order.all()
    """
    := signifi kon assignation  cart le result rekupére de ka rekéte puis on verifie si le panier existe ainsi de suite
    """
    if cart:=request.user.cart:
        
        cart.delete()
    return redirect('index')