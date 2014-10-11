from django.db import models

class CompanyMapping(models.Model):
    company_name = models.CharField(max_length=255)
    sector = models.CharField(max_length=255)
