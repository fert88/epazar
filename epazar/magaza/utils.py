import json
from .models import *
def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cartItems = order['get_cart_items']
    for i in cart:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
        for i in cart:
            try:
                cartItems += cart[i]['quantity']
                product = Product.objects.get(id=i)
                total = (product.price * cart[i]['quantity'])
                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']
                item = {
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'imageURL': product.imageURL,
                    },
                    'quantity': cart[i]['quantity'],
                    'get_total': total, }
                items.append(item)
            except:
                pass
    return {'items':items,'order':order,'cartItems':cartItems}
def cartData(request):
    if request.user.is_authenticated:
        costumer = request.user.costumer
        order, created = Order.objects.get_or_create(costumer=costumer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'items':items,'order':order,'cartItems':cartItems}
def guestOrder(request,data):
    print("Giriş yapınız!!!")
    print('Cookies:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    cookieData = cookieCart(request)
    items = cookieData['items']
    costumer, created = Costumer.objects.get_or_create(email=email,)
    costumer.name = name
    costumer.save()
    order = Order.objects.create(
        costumer=costumer,
        complete=False, )
    for item in items:
        product = Product.objects.get(id=item['product'][id])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
        )
    return [costumer, order]