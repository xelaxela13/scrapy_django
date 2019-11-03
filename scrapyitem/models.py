from django.db import models


class BaseScrapyModel(models.Model):
    f1 = models.TextField(blank=True, null=True)
    f2 = models.TextField(blank=True, null=True)
    f3 = models.TextField(blank=True, null=True)
    f4 = models.TextField(blank=True, null=True)
    f5 = models.TextField(blank=True, null=True)
    f6 = models.TextField(blank=True, null=True)
    f7 = models.TextField(blank=True, null=True)
    f8 = models.TextField(blank=True, null=True)
    f9 = models.TextField(blank=True, null=True)
    f10 = models.TextField(blank=True, null=True)


class TestScrapyModel(BaseScrapyModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
