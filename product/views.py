from django.shortcuts import render
from .models import Product
from django.views.generic import ListView, DetailView
from re import template
from django.shortcuts import render, redirect
from django.db.models import Q, Sum
from cart.cart import Cart
from django.http import HttpResponseRedirect
from django.contrib import messages


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['NewProducts'] = Product.objects.order_by('-date_created')[:4]
        # Dict = self.object.productaccessory_set.aggregate(Sum('product_price'))
        # context['Total_Accessory_Price'] = Dict['product_price__sum']
        # context = {'NewPrice': 12345}
        # context['Total_Accessory_Price']= "{:.2f}".format(Dict['product_price__sum'])
        return context


def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    messages.success(request, f'Successfully added product to cart!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'), )


def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


def cart_detail(request):
    return render(request, 'product/cart_detail.html')
