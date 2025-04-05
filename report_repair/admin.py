from django.contrib import admin
from report_repair.models import ReportStatus, Report, ReportImage


class ReportStatusAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "sequence"]
    ordering = ["-sequence"]


class ReportAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "equipment_type",
        "status",
        "title",
        "detail",
        "remark",
        "user",
        "staff",
        "created_at",
        "start_date",
        "end_date",
    ]
    ordering = ["-id"]
    list_filter = ["status"]


class ReportImageAdmin(admin.ModelAdmin):
    list_display = ["id", "report", "image"]
    ordering = ["-id"]


# Register your models here.
admin.site.register(ReportStatus, ReportStatusAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(ReportImage, ReportImageAdmin)
