from django.contrib import admin
from django.contrib.auth.models import Permission, User
from .models import Category, Institution, Donation

admin.site.register(Permission)
admin.site.empty_value_display = '(None)'


class UserAdmin(admin.ModelAdmin):
    model = User
    min_users = 2
    list_display = ['username', 'email']
    list_filter = ['username']

    def delete_queryset(self, request, queryset):

        all_users = self.model.objects.all()
        if queryset:
            users = all_users.exclude(pk__in=queryset)

        if users.count()<= self.min_users:
            message = 'Musi pozostać co najmniej {} user(ów).'
            self.message_user(request, message.format(self.min_users))
            return False
        if request.user in queryset:
            message = 'Nie możesz usunąć samego siebie.'
            self.message_user(request, message)
            return False
        return super().delete_queryset(request, queryset)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


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
