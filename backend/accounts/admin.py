from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Pet, TutorProfile, StaffProfile, VetSkills

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('user_type', 'phone', 'address', 'profile_picture')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Pet)
admin.site.register(TutorProfile)
admin.site.register(StaffProfile)
admin.site.register(VetSkills)
