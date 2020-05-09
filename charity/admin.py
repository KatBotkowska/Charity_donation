from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission, User
from .models import Category, Institution, Donation

# admin.site.register(User, UserAdmin)
admin.site.register(Permission)
admin.site.empty_value_display = '(None)'

#@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    min_users=1


    def has_delete_permission(self, request, obj=None):
        queryset = self.model.objects.all()
        selected = request.POST.getlist(helpers.ACTION_CHECKBOX_NAME)
        if selected:
            queryset = queryset.exclude(pk__in=selected)

        if queryset.count() <= self.min_objects:
            message = 'Musi pozostać co najmniej {} user(ów).'
            self.message_user(request, message.format(self.min_objects))
            return False
        if request.user in selected:
            message = 'Nie możesz usunąć samego siebie.'
            self.message_user(request, message)
            return False
        return super().has_delete_permission(request, obj)

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
