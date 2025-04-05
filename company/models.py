from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100, default="", blank=True, null=True, unique=True)
    image = models.ImageField(upload_to="company/images/", default="", blank=True)
    line_notify = models.CharField(
        max_length=255, default="", blank=True, null=True
    )

    def __str__(self):
        return f"{self.name}"