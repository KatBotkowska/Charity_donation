from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from .models import Category, Institution, Donation

# admin.site.register(User, UserAdmin)
admin.site.register(Permission)
admin.site.empty_value_display = '(None)'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    list_filter = ['name']


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'description', 'get_categories']
    list_filter = ['name']


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['institution', 'user', 'pick_up_date', 'pick_up_comment', 'quantity', 'get_categories', 'status',
                    'update_date']
    list_filter = ['institution', 'user', ]