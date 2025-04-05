from django.db import models
from django.contrib.auth.models import AbstractUser
from company.models import Company
from department.models import Department


# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=100, default="", blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class User(AbstractUser):
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        related_name="user_company",
        blank=True,
        null=True,
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        related_name="user_department",
        blank=True,
        null=True,
    )
    emp_id = models.CharField(max_length=10, default="", blank=True)
    tel = models.CharField(max_length=10, default="", blank=True)
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        related_name="user_role",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.username}"
