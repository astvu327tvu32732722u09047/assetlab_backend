from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import AdminUser

@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'is_superadmin', 'created_at')
    search_fields = ('email',)
    readonly_fields = ('created_at',)

    def save_model(self, request, obj, form, change):
        # hash password only when creating or changing password
        if not change or 'password' in form.changed_data:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)
