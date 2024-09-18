from django.shortcuts import render, HttpResponse
from .task import test_task
from .models import Product
# Create your views here.

def Home(request):
    products = Product.objects.filter(is_post=True)
    return render(request, 'home.html', context={'products':products})