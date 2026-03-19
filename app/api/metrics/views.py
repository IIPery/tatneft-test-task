from rest_framework import generics
from django.shortcuts import get_object_or_404
from app.core.models import Metric, MetricRecord, Tag
from app.api.metrics.serializers import MetricSerializer, MetricRecordSerializer, TagSerializer


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class MetricListCreateView(generics.ListCreateAPIView):
    serializer_class = MetricSerializer

    def get_queryset(self):
        return Metric.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MetricRecordListCreateView(generics.ListCreateAPIView):
    serializer_class = MetricRecordSerializer

    def get_queryset(self):
        metric_id = self.kwargs['metric_id']
        return MetricRecord.objects.filter(metric_id=metric_id, metric__user=self.request.user)

    def perform_create(self, serializer):
        metric_id = self.kwargs['metric_id']
        metric = get_object_or_404(Metric, id=metric_id, user=self.request.user)

        serializer.save(metric=metric)


class MetricRecordDetailView(generics.RetrieveAPIView):
    serializer_class = MetricRecordSerializer
    lookup_url_kwarg = 'record_id'

    def get_queryset(self):
        metric_id = self.kwargs['metric_id']
        return MetricRecord.objects.filter(metric_id=metric_id, metric__user=self.request.user)
