from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from accounts.models import User, Friend_Request, Chat_Users

# Register your models here.
class MyUserAdmin(UserAdmin):
    model = User

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'location', 
                           'birth_date',
                             'friends', 'slug')}),
        )
    prepopulated_fields = {"slug": ("username",)}

admin.site.register(User, MyUserAdmin)
admin.site.register(Friend_Request)
admin.site.register(Chat_Users)
