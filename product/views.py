from django.shortcuts import render
from .models import Product
from django.views.generic import ListView, DetailView
from re import template
from django.shortcuts import render, redirect
from django.db.models import Q, Sum
from cart.cart import Cart
from django.http import HttpResponseRedirect
from django.contrib import messages
from user.forms import VisitorMessagesForm


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

class ProductListView(ListView):
    model = Product
    template_name = 'product/product_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        et = super(ProductListView, self).get_context_data(**kwargs)
        et['products'] = Product.objects.order_by('-date_created')[:12]
        et['NewProducts'] = Product.objects.order_by('-date_created')[:4]
        et['v_form'] = VisitorMessagesForm()
        return et

# start of cart
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
# end of cart



# start of product list filter
def ProductList(request):
    if request.method == 'POST':
        if request.POST.get('RadioCourse'):
            template_name = 'products'
            value = request.POST.get('RadioCourse')
            sort_by = value
            if sort_by == "all_level":
                # dc means date created
                products = Product.objects.order_by('-date_created')[:12]
                R = 'all_level'
                context = {
                    'products': products,
                    'radio': R

                }
            elif sort_by == "beginner":
                # lp means low to high product price
                products = Product.objects.filter(level='Beginner')
                R = 'beginner'
                context = {
                    'products': products,
                    'radio': R

                }
            elif sort_by == "Intermediate":
                # hp means high to low product price
                products = Product.objects.filter(level='Intermediate')
                R = 'Intermediate'
                context = {
                    'products': products,
                    'radio': R

                }
            elif sort_by == "Expert":
                products = Product.objects.filter(level='Expert')
                R = 'Expert'
                context = {
                    'products': products,
                    'radio': R
                }
    else:
        products = Product.objects.all()
        context = {
            'products': products,
        }
    return render(request, 'product/product_list.html', context)

# end of product list filter
