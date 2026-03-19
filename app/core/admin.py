from django.contrib import admin

from app.core.models import Metric, MetricRecord, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "description")
    search_fields = ("user", "name", "description")


@admin.register(MetricRecord)
class MetricRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "metric__name", "value", "timestamp")
    search_fields = ("metric__name", "value", "timestamp")
    list_filter = ("tags",)
