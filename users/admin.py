from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users import models


# Register your models here.
@admin.register(models.CustomUser)
class CustomUserAdmin(UserAdmin, admin.ModelAdmin[models.CustomUser]):
    pass
