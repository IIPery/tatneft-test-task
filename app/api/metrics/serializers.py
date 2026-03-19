from rest_framework import serializers
from app.core.models import Metric, MetricRecord, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ['id', 'name', 'description']


class MetricRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricRecord
        fields = ['id', 'value', 'timestamp', 'tags']