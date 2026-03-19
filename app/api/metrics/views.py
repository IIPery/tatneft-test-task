from django.core.cache import cache
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response

from app.api.metrics.serializers import MetricRecordSerializer, MetricSerializer, TagSerializer
from app.core.models import Metric, MetricRecord, Tag


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class MetricListCreateView(generics.ListCreateAPIView):
    serializer_class = MetricSerializer

    def get_queryset(self) -> QuerySet:
        return Metric.objects.filter(user=self.request.user)

    def perform_create(self, serializer: MetricSerializer) -> None:
        serializer.save(user=self.request.user)


class MetricRecordListCreateView(generics.ListCreateAPIView):
    serializer_class = MetricRecordSerializer

    def get_queryset(self) -> QuerySet:
        metric_id = self.kwargs["metric_id"]
        return MetricRecord.objects.filter(metric_id=metric_id, metric__user=self.request.user)

    def list(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        metric_id = self.kwargs["metric_id"]
        cache_key = f"metric_records_{metric_id}"

        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)

        cache.set(cache_key, response.data, timeout=300)
        return response

    def perform_create(self, serializer: MetricRecordSerializer) -> None:
        metric_id = self.kwargs["metric_id"]
        metric = get_object_or_404(Metric, id=metric_id, user=self.request.user)

        serializer.save(metric=metric)

        cache_key = f"metric_records_{metric_id}"
        cache.delete(cache_key)


class MetricRecordDetailView(generics.RetrieveAPIView):
    serializer_class = MetricRecordSerializer
    lookup_url_kwarg = "record_id"

    def get_queryset(self) -> QuerySet:
        metric_id = self.kwargs["metric_id"]
        return MetricRecord.objects.filter(metric_id=metric_id, metric__user=self.request.user)
