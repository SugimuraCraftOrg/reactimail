from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.timezone import localtime
from django.utils.translation import gettext_lazy as _
from .models import ReactiMailUser


@admin.register(ReactiMailUser)
class ReactiMailUserAdmin(UserAdmin):
    model = ReactiMailUser
    list_display = (
        "email",
        "nickname",
        "is_superuser",
        "is_staff",
        "is_active",
        "formatted_last_login",
        "formatted_created_at",
    )
    list_filter = ("is_staff", "is_active")
    ordering = ("email", "is_active")
    search_fields = ("email", "nickname")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("nickname",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )

    def formatted_last_login(self, obj):
        """Customize datetime format of last_login."""
        return (
            localtime(obj.last_login).strftime("%Y-%m-%d %H:%M:%S")
            if obj.last_login
            else "N/A"
        )

    formatted_last_login.short_description = "Last Login"  # type: ignore
    formatted_last_login.admin_order_field = "last_login"  # type: ignore

    def formatted_created_at(self, obj):
        """Customize datetime format of created_at."""
        return (
            localtime(obj.created_at).strftime("%Y-%m-%d %H:%M:%S")
            if obj.created_at
            else "N/A"
        )

    formatted_created_at.short_description = "Created At"  # type: ignore
    formatted_created_at.admin_order_field = "created_at"  # type: ignore
