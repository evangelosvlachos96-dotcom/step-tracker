from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models import *


class CustomUserAdmin(UserAdmin):
    model = User


admin.site.register(User, CustomUserAdmin)
admin.site.register(DaySteps)
