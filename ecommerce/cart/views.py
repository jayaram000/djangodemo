from django.shortcuts import render,redirect
from shop.models import Product
from cart.models import Cart,Order,Account
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def cartview(request):
    u=request.user
    cart=Cart.objects.filter(user=u)
    total=0
    for i in cart:
        total+=i.quantity*i.product.price

    return render(request,'cartview.html',{'c':cart,'t':total})



@login_required

def addtocart(request,n):
    p=Product.objects.get(name=n)
    u=request.user#current login user
    try:
        cart=Cart.objects.get(user=u,product=p) #it checks if product is already added to cart else except will work
        if(p.stock > 0):
            cart.quantity+=1  # it add one quantity to that particular product
            cart.save()
            p.stock-=1  #after adding quantity and the quantity of that particular product is taken from the stock field so we also need to decrease the stock of that product
            p.save()
    except:
        if(p.stock > 0):
            cart=Cart.objects.create(product=p,user=u,quantity=1) #when we adding first time a product to cart so this will create a cart of that particular product with one quantity
            cart.save()
            p.stock-=1
            p.save()
    return cartview(request)


@login_required
def remove_quantity(request,n):
    p=Product.objects.get(name=n)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(cart.quantity>1):
            cart.quantity-=1
            cart.save()
            p.stock+=1
            p.save()

        else:
            cart.delete()
            p.stock += 1
            p.save()
    except:
        pass

    return cartview(request)


@login_required
def delete_item(request,n):
    p=Product.objects.get(name=n)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        cart.delete()
        p.stock+=cart.quantity
        p.save()
    except:
        pass

    return cartview(request)




@login_required
def orderform(request):
    if (request.method=='POST'):
        a=request.POST['a']
        p = request.POST['p']
        n = request.POST['n']

        u=request.user
        cart=Cart.objects.filter(user=u)

        total=0
        for i in cart:
            total+=i.quantity*i.product.price

        try:
            ac=Account.objects.get(acctnum=n)
            if (ac.amount >= total):
                ac.amount-=total
                ac.save()
                for i in cart:
                    o=Order.objects.create(user=u,product=i.product,address=a,phone=p,no_of_items=i.quantity,order_status="paid")
                    o.save()
                cart.delete()
                msg="order placed successfully"
                return render(request,'orderdetail.html',{'msg':msg})
            else:
                msg = "Due to insufficient fund cant place order"
                return render(request, 'orderdetail.html', {'msg': msg})
        except:
            pass
    return render(request,'orderform.html')



@login_required
def orderview(request):
    u=request.user
    o=Order.objects.filter(user=u)

    return render(request,'orderview.html',{'orders':o})












