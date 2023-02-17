from django.shortcuts import render
from product.models import Product
from django.views.generic import ListView, DetailView
from re import template
from django.shortcuts import render, redirect
from user.forms import VisitorMessagesForm
from django.db.models import Q, Sum
from django.contrib import messages
from blog.models import Blog

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
        et['v_form'] = VisitorMessagesForm()
        et['blogs'] = Blog.objects.order_by('-date_created')[:3]
        return et


def VisitorMessages(request):
    if request.method == 'POST':
        v_form = VisitorMessagesForm(request.POST)
        if v_form.is_valid():
            v_form.save()
            messages.success(request, f'Your message has been sent')
            return redirect('index')
        else:
            messages.warning(request, f'An error occurred! Kindly try again.')
            return redirect('index')
        messages.warning(request, f'An error occurred! Kindly try again.')
        return redirect('index')

    else:
        messages.warning(request, f'An error occurred! Kindly try again.')
        return redirect('index')
