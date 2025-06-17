from django.contrib import admin
from .models import CustomUser

admin.site.register(CustomUser)

# --------------------- block user

# from django.contrib.auth.admin import UserAdmin

# class CustomUserAdmin(UserAdmin):
#     list_display = ('email', 'role', 'is_active', 'is_staff', 'is_blocked')  # List view columns
#     list_filter = ('role', 'is_blocked', 'is_active', 'is_staff')
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin', 'is_superadmin', 'is_blocked')}),
#         ('Role', {'fields': ('role',)}),
#     )
#     search_fields = ('email',)
#     ordering = ('email',)
#     filter_horizontal = ()

# admin.site.register(CustomUser, CustomUserAdmin)


# ---------------------------------