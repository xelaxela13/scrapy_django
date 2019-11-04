from django.db import models


class AbstractBaseScrapyModel(models.Model):
    class Meta:
        abstract = True

    domain = models.CharField(max_length=255, blank=False, null=False)
    url = models.CharField(max_length=255, blank=False, null=False)
    spider_name = models.CharField(max_length=255, blank=False, null=False)
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


class TestScrapyModel(AbstractBaseScrapyModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    site = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
