from django.contrib import admin
from .models import ProductImage, Product, ProductCategory

# Register your models here.

class ProductCategoryAdmin(admin.ModelAdmin):
    model = ProductCategory

admin.site.register(ProductCategory, ProductCategoryAdmin)


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage



# this class define which department columns will be shown in the department admin web site.
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
    # a list of displayed columns name.
    list_display = ['product_name', 'price', 'id']

    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)
