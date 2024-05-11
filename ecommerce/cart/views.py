from django.shortcuts import render,redirect
from django.http import HttpResponse
from shop.models import Product
from cart.models import Cart,Order,Account
from django.contrib.auth.decorators import login_required

@login_required
def cart_view(request,user,product):
    #for displaying cart for the current user
    u=request.user
    total=0
    c=Cart.objects.filter(user=u)
    #to find the total amount
    for i in c:
        total=total+i.quantity*i.product.price

    return render(request,'cart.html',{'c':c,'total':total})


@login_required


def addtocart(request,p): #for adding a particular product to cart table
    p=Product.objects.get(id=p)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(p.stock>0):
           cart.quantity+=1
           cart.save()
           p.stock-=1
           p.save()
    except:
        if (p.stock >0):

           cart=Cart.objects.create(product=p,user=u,quantity=1)
           cart.save()
           p.stock -= 1
           p.save()

    return cart_view(request)

def cart_remove(request,p):
    p = Product.objects.get(id=p)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)

        if(cart.quantity>1):
           cart.quantity -= 1
           cart.save()
           p.stock += 1
           p.save()

        else:
            cart.delete()
            p.stock += 1
            p.save()
    except:
        pass

    return cart_view(request)


def full_remove(request,p):
    p = Product.objects.get(id=p)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        cart.delete()
        p.stock += cart.quantity
        p.save()
    except:
        pass



    return cart_view(request)

# @login_required
#
# def orderform(request,):
#     if(request.method=="POST"):
#         a=request.POST['a']
#         p=request.POST['p']
#         n=request.POST['n']
#         u=request.user
#
#         c=Cart.objects.filter(user=u)
#
#         total=0
#         for i in c:
#             total=total+i.quantity*i.product.price
#
#         try:
#             ac=Account.objects.get(acctnum=n)
#             if(ac.amount >= total):
#                 ac.amount =ac.amount-total
#                 ac.save()
#                 for i in c:
#                     o=Order.objects.create(user=u,product=i.product,address=a,phone=p,no_of_items=i.quantity,order_status="paid")
#                     o.save()
#
#                 c.delete()
#                 msg="Order placed Succesfully"
#                 return render(request,'orderdetail.html',{'message':msg})
#             else:
#                 msg = "Insufficient Amount.You can't Place Order"
#                 return render(request, 'orderdetail.html', {'message': msg})
#
#
#         except:
#             pass
#
#
#         return render(request,'orderform.html')


@login_required
def orderform(request):
    if request.method == "POST":
        # Process the form submission
        a = request.POST.get('a', '')
        p = request.POST.get('p', '')
        n = request.POST.get('n', '')
        u = request.user

        # Retrieve items from cart and calculate total
        c = Cart.objects.filter(user=u)
        total = sum(item.quantity * item.product.price for item in c)

        try:
            ac = Account.objects.get(acctnum=n)
            if ac.amount >= total:
                ac.amount -= total
                ac.save()
                for item in c:
                    order = Order.objects.create(
                        user=u,
                        product=item.product,
                        address=a,
                        phone=p,
                        no_of_items=item.quantity,
                        order_status="paid"
                    )
                    order.save()

                c.delete()
                msg = "Order placed successfully"
                return render(request, 'orderdetail.html', {'message': msg})
            else:
                msg = "Insufficient amount. You can't place the order."
                return render(request, 'orderdetail.html', {'message': msg})

        except Account.DoesNotExist:
            msg = "Invalid account number."
            return render(request, 'orderdetail.html', {'message': msg})

    # If it's not a POST request, render the order form page
    return render(request, 'orderform.html')


@login_required
def orderview(request):
    u=request.user
    o=Order.objects.filter(user=u)

    return render(request,'orderview.html',{'o':o,'u':u.username})