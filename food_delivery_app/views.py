from django.shortcuts import render, HttpResponse
from .task import test_task
# Create your views here.

def Home(request):
    # result = test_task.apply_async()
    # print(result)
    return render(request, 'home.html', context={})