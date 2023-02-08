from django.shortcuts import render
from product.models import Product
from django.views.generic import ListView, DetailView
from re import template
from django.shortcuts import render, redirect
from django.db.models import Q, Sum
from django.contrib import messages

# Create your views here.


def AboutUs(request):
    return render(request, 'main/about_us.html')


# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = 'main/index.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        et = super(ProductListView, self).get_context_data(**kwargs)
        et['products'] = Product.objects.order_by('-date_created')[:12]
        et['NewProducts'] = Product.objects.order_by('-date_created')[:4]
        return et
