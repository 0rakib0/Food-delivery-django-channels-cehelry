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