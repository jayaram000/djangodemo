from django.shortcuts import render,redirect
from shop.models import Category,Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required



def all_categories(request):
    c=Category.objects.all()
    return render(request,'category.html',{'c':c})

@login_required
def products(request,p):
    c=Category.objects.get(name=p)
    p=Product.objects.filter(category=c)
    return render(request,'products.html',{'c':c,'p':p})


@login_required
def detail(request,p):
    p=Product.objects.get(name=p)
    return render(request,'detail.html',{'p':p})


def register(request):
    if(request.method=="POST"):

        u=request.POST['u']
        p = request.POST['p']
        cp = request.POST['cp']
        fn = request.POST['fn']
        ln = request.POST['ln']
        e = request.POST['e']

        if(cp==p):
            u=User.objects.create_user(username=u,password=p,first_name=fn,last_name=ln,email=e)
            u.save()
            return redirect('shop:allcat')
    return render(request,'register.html')


def user_login(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']
        user=authenticate(username=u,password=p)
        if user:
            login(request,user)
            return redirect('shop:allcat')
        else:
            return HttpResponse("Invalid Credentials")
    return render(request,'login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('shop:login')




