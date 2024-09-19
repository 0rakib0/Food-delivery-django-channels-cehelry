from django.shortcuts import render, HttpResponse
from .task import test_task
from .models import Product
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Product, Order
# Create your views here.

def Home(request):
    products = Product.objects.filter(is_post=True)
    return render(request, 'home.html', context={'products':products})


def OrderList(request):
    user = request.user 
    try:
        order = Order.objects.filter(user=user)
    except Order.DoesNotExist:
        pass      
    return render(request, 'orderlist.html', context={'order_list':order})  


@csrf_exempt
def OrderApi(request):
    data = json.loads(request.body)
    id = data['id']
    user = request.user
    try:
        product = Product.objects.get(id=id)
        order = Order(
            user=user,
            item=product,
            total_amount = product.price
        )
        order.save()
        return JsonResponse({'msg':'Order succefully receive', 'status':True})
    except Product.DoesNotExist():
        return JsonResponse ({'msg':'Something went rong!', 'status':False})
    
def OrderView(request, id):
    user = request.user 
    print(id)
    try:
        order = Order.objects.filter(id=id, user=user).first()
    except Order.DoesNotExist:
        pass
    
    return render(request, 'order_view.html', context={'order':order})