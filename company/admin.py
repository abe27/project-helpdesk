from django.contrib import admin
from .models import Company


class CompanyAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "image"]
    ordering = ["-id"]


# Register your models here.
admin.site.register(Company, CompanyAdmin)

