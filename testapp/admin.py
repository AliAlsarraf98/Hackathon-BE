from django.contrib import admin

from testapp import models


# Register your models here.
@admin.register(models.TestApp)
class TestAppAdmin(admin.ModelAdmin[models.TestApp]):
    pass
