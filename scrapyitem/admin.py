import csv
import json

from dicttoxml import dicttoxml
from django.contrib import admin
from django.contrib.admin import register
from django.utils.timezone import datetime
from django.contrib import messages

from scrapyitem.models import TestScrapyModel


@register(TestScrapyModel)
class ScrapyResult(admin.ModelAdmin):
    actions = ('save_to_csv', 'save_to_xml', 'save_to_json')
    ordering = ('id',)
    list_filter = ('domain', 'spider_name')
    list_display = ('domain', 'created')

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.get_fields() if f.name != 'id']

    def save_to_csv(self, request, queryset):
        exclude_fields = {}
        filename = 'results/' + self.model.__name__ + datetime.now().strftime('-%d-%m-%Y') + '.csv'
        fieldnames = [f.name for f in self.model._meta.get_fields() if f.name not in exclude_fields]
        with open(filename, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for i in queryset.values(*fieldnames):
                writer.writerow(i)
            messages.add_message(request, messages.SUCCESS, f'{filename} was saved')

    def save_to_xml(self, request, queryset):
        exclude_fields = {}
        filename = 'results/' + self.model.__name__ + datetime.now().strftime('-%d-%m-%Y') + '.xml'
        fieldnames = [f.name for f in self.model._meta.get_fields() if f.name not in exclude_fields]
        with open(filename, 'wb') as f:
            xml = dicttoxml(queryset.values(*fieldnames), custom_root='root', attr_type=False)
            f.write(xml)
            messages.add_message(request, messages.SUCCESS, f'{filename} was saved')

    def save_to_json(self, request, queryset):
        exclude_fields = {}
        filename = 'results/' + self.model.__name__ + datetime.now().strftime('-%d-%m-%Y') + '.json'
        fieldnames = [f.name for f in self.model._meta.get_fields() if f.name not in exclude_fields]
        with open(filename, 'w') as f:
            json_data = json.dumps(list(queryset.values(*fieldnames)), ensure_ascii=False)
            f.write(json_data)
            messages.add_message(request, messages.SUCCESS, f'{filename} was saved')
