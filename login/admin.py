from django.contrib import admin
from login.models import User

# Register your models here.
class UserInLine(admin.StackedInline):
    model = User
    extra = 2

class UserAdmin(admin.ModelAdmin):

    ist_display = ('name', 'email', 'last_login_date')
    inlines = [UserInLine]

    search_fields = ['name']

admin.site.register(User, UserAdmin)