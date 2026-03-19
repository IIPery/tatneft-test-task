from rest_framework import generics
from rest_framework.response import Response
from django.core.cache import cache
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

    def list(self, request, *args, **kwargs):
        metric_id = self.kwargs['metric_id']
        cache_key = f"metric_records_{metric_id}"

        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)

        cache.set(cache_key, response.data, timeout=300)
        return response

    def perform_create(self, serializer):
        metric_id = self.kwargs['metric_id']
        metric = get_object_or_404(Metric, id=metric_id, user=self.request.user)

        serializer.save(metric=metric)

        cache_key = f"metric_records_{metric_id}"
        cache.delete(cache_key)


class MetricRecordDetailView(generics.RetrieveAPIView):
    serializer_class = MetricRecordSerializer
    lookup_url_kwarg = 'record_id'

    def get_queryset(self):
        metric_id = self.kwargs['metric_id']
        return MetricRecord.objects.filter(metric_id=metric_id, metric__user=self.request.user)
