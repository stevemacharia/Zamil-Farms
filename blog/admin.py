from django.contrib import admin
from .models import Blog


# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    model = Blog

admin.site.register(Blog, BlogAdmin)


