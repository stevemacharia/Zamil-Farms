from django.contrib import admin
# Register your models here.
from .models import Order, OrderDetail


# Register your models here.


class OrderDetailsAdmin(admin.StackedInline):
    model = OrderDetail


# this class define which department columns will be shown in the department admin web site.
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderDetailsAdmin]
    # a list of displayed columns name.
    list_display = ['order_name_id', 'status', 'customer_id', 'payment_method', 'order_amount', 'date_ordered']
    # list_filter = ('p',)
    # define search columns list, then a search box will be added at the top of Department list page.
    search_fields = ['order_name_id', 'customer_id', ]
    # define model data list ordering.
    ordering = ('date_ordered',)


admin.site.register(Order, OrderAdmin)
