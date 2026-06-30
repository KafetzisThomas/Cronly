from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "is_active", "is_superuser", "date_joined", "last_login")
    list_filter = ("is_active", "is_superuser")
    fieldsets = UserAdmin.fieldsets + (("Notifications", {"fields": ("discord_webhook_url",)}),)
    search_fields = ("username",)
    ordering = ("username",)
