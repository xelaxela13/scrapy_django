import csv
from django.contrib import admin
from django.contrib.admin import register
from django.utils.timezone import datetime
from django.contrib import messages

from scrapyitem.models import TestScrapyModel


@register(TestScrapyModel)
class ScrapyResult(admin.ModelAdmin):
    fields = ('name', 'city', 'phone')
    actions = ('save_to_csv',)
    ordering = ('id',)

    def save_to_csv(self, request, queryset):
        exclude_fields = {}
        filename = 'results/' + self.model.__name__ + datetime.now().strftime('-%d-%m-%Y') + '.csv'
        with open(filename, 'w') as f:
            fieldnames = [f.name for f in self.model._meta.get_fields() if f.name not in exclude_fields]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for i in queryset.values(*fieldnames):
                writer.writerow(i)
            messages.add_message(request, messages.SUCCESS, f'{filename} was saved')
