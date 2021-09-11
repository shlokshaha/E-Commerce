import json
from .models import *


#we need to repeat this code in all views which causes more redundancy
def cookieCart(request):            #logic for guest users
    try:
        cart = json.loads(request.COOKIES['cart'])  # get the cookie and convert it to dictionary
    except:  # if no cookie create empty cookie
        cart = {}
    print("Cart:", cart)
    items = []
    order = {'get_total_cart_items': 0, 'get_cart_total': 0, 'shipping': False}
    cartItems = order['get_total_cart_items']

    for i in cart:  # looping dict
        try:  # if product gets deleted from db, we cant query it so it throws error
            cartItems += cart[i]['quantity']  # get total items in cart (cookie)

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_total_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'get_order_item_total': total
            }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {'cartItems':cartItems, 'order':order, 'items':items}


def cartData(request):                         #actual view which repeats for each page
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_total_cart_items
    else:
        cookieData = cookieCart(request)        #function from same file
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems':cartItems, 'order':order, 'items':items}


def guestOrder(request, data):           #processing checkout order of guest users (from views.py to keep it clean)
    print("User is not logged in")
    print("COOKIES", request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    # store the guest users details in db *after checkout*
    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()
    order = Order.objects.create(customer=customer, complete=False)

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(order=order, product=product, quantity=item['quantity'])

    return customer,order