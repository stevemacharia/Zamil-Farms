from django.contrib import admin
from .models import UserProfile, Messages

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'profile_pic']
    # define search columns list, then a search box will be added at the top of Department list page.
    search_fields = ['names']

    # list_filter = ('status',)

    # define model data list ordering.
    # ordering = ('status')
    def email(self, obj):
        return obj.user.email

    class Meta:
        model = UserProfile


admin.site.register(UserProfile, UserProfileAdmin)




class MessagesAdmin(admin.ModelAdmin):
    list_display = ['username', 'status', 'email', 'message']
    # define search columns list, then a search box will be added at the top of Department list page.
    search_fields = ['username', 'email']
    list_filter = ('status',)
    # define model data list ordering.
    # ordering = ('status')


    class Meta:
        model = Messages


admin.site.register(Messages, MessagesAdmin)
