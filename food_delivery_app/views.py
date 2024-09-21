from django.shortcuts import render, HttpResponse, redirect
from .task import Email_send
from .models import Product
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Product, Order, Notification
from django.contrib.auth.models import User
# Create your views here.

def Home(request):
    products = Product.objects.filter(is_post=True)
    notification = Notification.objects.all()
    return render(request, 'home.html', context={'products':products, 'notification':notification})


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
    progress_percentage = Order.get_percentage(id)
    try:
        order = Order.objects.filter(id=id, user=user).first()
    except Order.DoesNotExist:
        pass
    
    return render(request, 'order_view.html', context={'order':order, 'progress_percentage':progress_percentage})



def UserList(request):
    users = User.objects.all()
    return render(request, 'users.html', context={'users':users})


def SendMail(request):
    if request.method == 'POST':
        email_sub = request.POST.get('sub')
        mail_content = request.POST.get('email_content')
       
        data = {}
        data['email_sub'] = email_sub
        data['mail_content'] = mail_content
        json_data = json.dumps(data)
        print(json_data)
        
        result = Email_send.apply_async(args=[(json_data,)])
        print(result)
        
    return redirect("home")