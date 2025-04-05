from django.db import models
from user.models import User
from equipment.models import EquipmentType
from django.utils import timezone


class ReportStatus(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    sequence = models.IntegerField(blank=True, null=True, unique=True)

    def __str__(self):
        return self.name


class Report(models.Model):
    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.SET_NULL,
        related_name="reports",
        blank=True,
        null=True,
    )
    title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="",
    )
    detail = models.TextField(blank=True, null=True, default="")
    status = models.ForeignKey(
        ReportStatus,
        on_delete=models.SET_NULL,
        related_name="reports",
        blank=True,
        null=True,
    )
    remark = models.TextField(blank=True, null=True, default="")
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="user_reports",
        blank=True,
        null=True,
    )
    staff = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="staff_reports",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=timezone.now())
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.id)
        # return self.title


class ReportImage(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="report/images/", blank=True, null=True)

    def __str__(self):
        return f"Image for report ID : {self.report.id}"


class RepairOutside(models.Model):
    report = models.ForeignKey(
        Report, on_delete=models.CASCADE, related_name="outside_repairs"
    )
    store = models.CharField(max_length=255, blank=True, null=True)
    remark = models.TextField(blank=True, null=True, default="")
    tel = models.CharField(max_length=10, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Repair outside for report ID : {self.report.id}"
