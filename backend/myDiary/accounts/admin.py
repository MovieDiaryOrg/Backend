from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import CustomUser


class UserAdmin(DefaultUserAdmin):
    # 목록에서 표시할 필드
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "phone",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
    )
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("email", "username", "first_name", "last_name", "phone")
    ordering = ("email",)

    # 사용자 세부 정보 보기
    readonly_fields = ("date_joined",)
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone")}),
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
        (
            "Important dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "first_name", "last_name", "phone", "password1", "password2"),
            },
        ),
    )


admin.site.register(CustomUser, UserAdmin)