from typing import ClassVar

from rest_framework import serializers

from app.core.models import Metric, MetricRecord, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields: ClassVar[list[str]] = ["id", "name"]


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields: ClassVar[list[str]] = ["id", "name", "description"]


class MetricRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricRecord
        fields: ClassVar[list[str]] = ["id", "value", "timestamp", "tags"]
