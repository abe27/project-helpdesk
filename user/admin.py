from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Role
from .form import UserForm
from django.urls import reverse
from django.utils.html import format_html


class UserAdmin(UserAdmin):
    form = UserForm  # ใช้ฟอร์มที่เราสร้างขึ้น

    def password_reset_link(self, obj):
        url = reverse("admin:auth_user_password_change", args=[obj.pk])
        return format_html('<a href="{}">Reset Password</a>', url)

    password_reset_link.short_description = "Reset Password"

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )

    fieldsets = (
        (None, {"fields": ("username",)}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "emp_id", "email", "tel", "role")},
        ),
        (
            "Additional info",
            {
                "fields": (
                    "company",
                    "department",
                )
            },
        ),
        (
            "Permissions",
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
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    def display_groups(self, obj):
        return ", ".join(group.name for group in obj.groups.all())

    display_groups.short_description = "Groups"

    list_display = (
        "id",
        "username",
        "email",
        "tel",
        "role",
        "password_reset_link",
        "first_name",
        "last_name",
        "display_groups",
        "company",
        "department",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    class Media:
        js = ("user/js/filterDept.js",)


class RoleAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


admin.site.register(User, UserAdmin)
admin.site.register(Role, RoleAdmin)
