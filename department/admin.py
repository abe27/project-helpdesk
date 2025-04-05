from django.contrib import admin
from .models import Department


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "company"]
    list_filter = ["company"]
    ordering = ["-company"]


# Register your models here.
admin.site.register(Department, DepartmentAdmin)
