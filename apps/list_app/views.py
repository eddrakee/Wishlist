from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Item
from ..login_app.models import User


# Create your views here.

def list_index(request):
    session_id = request.session['user_id']#this is from the register/login set_session
    all_data = Item.objects.get_all_data(session_id)
    context = {
        'all_data' : all_data,
    }
    return render(request, 'list_app/dashboard.html', context)

def add_item(request):
    return render(request, 'list_app/add_item.html')

def create_item(request):
    if len(request.POST['item_name'])< 3:
        messages.add_message(request, messages.ERROR, "Please enter a longer name. It must be at least 3 characters long!")
        return redirect ('list_ns:add')
    Item.objects.make_item(request.POST, request.session['user_id'])
    return redirect('list_ns:list_index')

def view_item(request, item_id):
    wishers = Item.objects.get_wishers(item_id)
    this_item = Item.objects.get_item_id(item_id)
    context = {
        'this_item' : this_item,
        'wishers' : wishers
    }
    print (context['this_item'])
    return render(request, 'list_app/show_item.html', context)

def add_wishlist(request, item_id):
    item_id=item_id
    user_id=request.session['user_id']
    print (user_id)
    Item.objects.add_wishlist(item_id, user_id)
    return redirect('list_ns:list_index')

def delete_item(request, item_id):
    Item.objects.delete_me(item_id)
    return redirect('list_ns:list_index')

def remove_item(request, item_id):
    Item.objects.remove_me(item_id, request.session['user_id'])
    return redirect('list_ns:list_index')

def logout(request):
    request.session.flush() #this clears all the sessions!
    return redirect('login_ns:user_index')

