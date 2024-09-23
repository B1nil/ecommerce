from django.shortcuts import render,redirect
from .models import Product
from .models import Cart,Order_table,Payment
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import razorpay

@login_required
def add_to_cart(request,i):
    p=Product.objects.get(id=i)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(p.stock>0):
            cart.quantity +=1
            cart.save()
            p.stock -=1
            p.save()
    except:
        if(p.stock):
            cart=Cart.objects.create(product=p,user=u,quantity=1)
            cart.save()
            p.stock -=1
            p.save()

    return redirect('cart:cart_view')

def cart_view(request):
    u=request.user
    cart=Cart.objects.filter(user=u)
    total=0
    for i in cart:
        total=total+i.quantity*i.product.price
    return  render(request,'cart.html',{'c':cart,'total':total})

def cart_decrement(request,i):
    p=Product.objects.get(id=i)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(Cart.quantity>1):
            cart.quantity -=1
            cart.save()
            p.stock+=1
            p.save()
        else:
            cart.delete()
            p.stock +=1
            p.save()
    except:
        pass
    return redirect('cart:cart_view')


def remove(request,i):
    p=Product.objects.get(id=i)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        cart.delete()
        p.save()
    except:
        pass
    return redirect('cart:cart_view')

def place_order(request):
    if(request.method=='POST'):
        p = request.POST.get('p')
        a = request.POST.get('a')
        n = request.POST.get('n')
        u = request.user
        c = Cart.objects.filter(user=u)
        total=0
        for i in c:
            total=total+(i.quantity*i.product.price)
            totat=int(total*100)#total amt

            #create razorpay  client using our API credentials

            client = razorpay.Client(auth=('rzp_test_KjG8ydENFtiZ4P','YFjiW3CMX7Z1Pq164lgbzKrm'))

        #create order in razorpay
        response_payment=client.order.create(dict(amount=total,currency='INR'))
        print(response_payment)
        return render(request,'place_order.html')

    return render(request,'place_order.html')

