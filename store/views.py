from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_total_cart_items
    else:
        items=[]
        order= {'get_total_cart_items':0 , 'get_cart_total':0, 'shipping':False}
        cartItems = order['get_total_cart_items']

    products = Product.objects.all()
    context = {'products':products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_total_cart_items
    else:
        items=[]
        order= {'get_total_cart_items':0 , 'get_cart_total':0, 'shipping':False}
        cartItems = order['get_total_cart_items']
    context = {'items':items, 'order':order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_total_cart_items
    else:
        items=[]
        order= {'get_total_cart_items':0 , 'get_cart_total':0, 'shipping':False}
        cartItems = order['get_total_cart_items']
    context = {'items':items, 'order':order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)         # converts json str into python dict
    productId = data['productId']
    action = data['action']
    print("Action:",action)
    print("Product ID:",productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)   # because we need to just change the value of orderItem quantity if it already exists

    if action=='add':
        orderItem.quantity+=1
    elif action=='remove':
        orderItem.quantity-=1

    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse('Item was Added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = data['form']['total']
        order.transaction_id = transaction_id
        order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                pincode=data['shipping']['pincode']
            )
    else:
        print("User is not logged in")
    return JsonResponse('Payment Complete', safe=False)