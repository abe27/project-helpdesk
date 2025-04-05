from django.db import models
from company.models import Company


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100, default="", blank=True, null=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="companies"
    )

    def __str__(self):
        return f"{self.name}"
