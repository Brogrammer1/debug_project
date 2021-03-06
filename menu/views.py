from operator import attrgetter

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from .forms import *
from .models import *


def menu_list(request):
    """displays all the menus on the root url page"""
    all_menus = Menu.objects.prefetch_related('items').all()
    menus = []
    menus2 = []

    for menu in all_menus:
        if menu.expiration_date:
            if menu.expiration_date >= timezone.now():
                menus.append(menu)
        else:
            menus2.append(menu)

    menus = sorted(menus, key=attrgetter('expiration_date'))
    menus = menus + menus2
    return render(request, 'menu/list_all_current_menus.html',
                  {'menus': menus})


def item_list(request):
    """displays a list of all items to items page """
    items = Item.objects.all()
    return render(request, 'menu/item_list.html', {'items': items})


def menu_detail(request, pk):
    """ displays chosen menu in more detail """
    menu = Menu.objects.get(pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    """displays chosen item in more detail"""
    try:
        item = Item.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'menu/detail_item.html', {'item': item})


def create_new_menu(request):
    """ displays form to create a new menu """
    if request.method == "POST":
        form = ChangeMenuForm(request.POST)
        if form.is_valid():
            menu = form.save()
            return redirect('menu_detail', pk=menu.pk)
    else:
        form = ChangeMenuForm()
    return render(request, 'menu/menu_edit.html', {'form': form})


def edit_menu(request, pk):
    """ displays form to edit menu """
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == "POST":
        form = ChangeMenuForm(request.POST, instance=menu)
        if form.is_valid():
            form.save()

            return redirect('menu_detail', pk=menu.pk)
    else:
        form = MenuForm(instance=menu)
    return render(request, 'menu/menu_edit.html', {'form': form})


def edit_item(request, pk):
    """ displays form to edit item """
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        form = ItemEditForm(request.POST, instance=item)
        if form.is_valid():
            form.save()

            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemEditForm(instance=item)
    return render(request, 'menu/item_edit.html', {'form': form})
