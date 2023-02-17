from django.shortcuts import render
from django.views.generic import ListView, DetailView
from blog.models import Blog


# Create your views here.
class ProductListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'blogs'

    def get_context_data(self, **kwargs):
        et = super(ProductListView, self).get_context_data(**kwargs)
        et['blogs'] = Blog.objects.order_by('-date_created')[:3]
        return et


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context