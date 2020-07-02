from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
import datetime
from .utils import cookieCart,cartData,guestOrder


def magaza(request):
    products=Product.objects.all()
    data = cartData(request)
    cartItems = data['cartItems']
    context = {'products': products,'cartItems':cartItems}
    return render(request, 'magaza/magaza.html', context)


def sepet(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request, 'magaza/sepet.html', context)


def cikis(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order,'cartItems':cartItems}
    return render(request, 'magaza/cikis.html', context)


def anasayfa(request):
    products = Product.objects.all()
    data = cartData(request)
    cartItems = data['cartItems']
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'magaza/anasayfa.html', context)
def updateItem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    print('productId',productId,'action',action)
    costumer=request.user.costumer
    product=Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(costumer=costumer, complete=False)
    orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)
    if action=='add':
        orderItem.quantity=orderItem.quantity+1
    elif action=='remove':
        orderItem.quantity=orderItem.quantity-1
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()
    return JsonResponse('item was added' , safe=False)
def proccessOrder(request):
    transaction_Id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    if request.user.is_authenticated:
        costumer=request.user.costumer
        order, created = Order.objects.get_or_create(costumer=costumer, complete=False)
    else:
       costumer=guestOrder(request,data)[0]
       order=guestOrder(request,data)[1]
    total = float(data['form']['total'])
    order.transaction_id = transaction_Id
    if total == order.get_cart_total:
        order.complete = True
    order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(
            costumer=costumer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    return JsonResponse('paymen complete', safe=False)
# Create your views here.
