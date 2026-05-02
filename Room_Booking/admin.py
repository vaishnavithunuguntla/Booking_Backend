

# from django.contrib import admin
# from .models import User

# from .models import Room,OccupiedDate,RoomImage
# # Register your models here.
# # Register your models here.
# # this willmake sure we will see it in admin panel
# admin.site.register(Room)
# admin.site.register(User)
# admin.site.register(OccupiedDate)
# admin.site.register(RoomImage)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Room, RoomImage, OccupiedDate

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "full_name", "is_staff", "is_superuser")
    search_fields = ("email", "full_name")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("full_name",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "password1", "password2", "is_staff", "is_superuser"),
        }),
    )

admin.site.register(Room)
admin.site.register(RoomImage)
admin.site.register(OccupiedDate)
