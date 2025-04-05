from django.contrib import admin
from equipment.models import EquipmentType

# Register your models here.
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "sequence"]
    ordering = ["-sequence"]
    
# Register your models here.
admin.site.register(EquipmentType, EquipmentTypeAdmin)