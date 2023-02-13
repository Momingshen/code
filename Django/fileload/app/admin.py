from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from app.models import MyUser

ADDITIONAL_FIELDS = ((None, {'fields': ('department_name','real_name','power_list')}),)

class MyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ADDITIONAL_FIELDS
    add_fieldsets = UserAdmin.fieldsets + ADDITIONAL_FIELDS

admin.site.register(MyUser, MyUserAdmin)