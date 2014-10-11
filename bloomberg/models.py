from django.db import models


class Company(models.Model):
    title = models.CharField(max_length=255)
    sector = models.CharField(max_length=255)
    key = models.CharField(max_length=255)