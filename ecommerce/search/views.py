from django.shortcuts import render
from shop.models import Product
from django.db.models import Q
def searchproducts(request):
    p=None
    query=""
    if(request.method=="POST"):
        Query=request.POST['q']
        if Query:
            p=Product.objects.filter(Q(name__icontains=Query)| Q(desc__icontains=Query))
    return render(request,'search.html',{'p':p,'q':query})
