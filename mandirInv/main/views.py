from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.http import HttpResponse
from .models import ToDoList, Item

User = get_user_model()


# Create your views here.
def index(response, id):
    ls = ToDoList.objects.get(id=id)
    # items = ls.item_set.get(id=id)
    return render(response, "main/list.html", {"ls": ls})


def home(request):
    context = {"user": request.user}

    return render(request, "main/home.html", context)
