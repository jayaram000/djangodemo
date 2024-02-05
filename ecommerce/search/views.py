from django.shortcuts import  render,redirect
from shop.models import Product,Category
from django.db.models import Q



def search(request):
    query = ""
    products = None
    if (request.method == "POST"):
        query = request.POST['q']
        if (query):
            products = Product.objects.filter(Q(name__icontains=query) | Q(desc__icontains=query) | Q(category__name__icontains=query))

    return render(request, 'search.html', {'query': query, 'b': products})

