from django.urls import path

from app.api.metrics.views import MetricListCreateView, MetricRecordDetailView, MetricRecordListCreateView, TagListView

app_name = "metrics"

urlpatterns = [
    path("tags/", TagListView.as_view(), name="tags-list"),
    path("metrics/", MetricListCreateView.as_view(), name="metrics-list"),
    path("metrics/<int:metric_id>/records/", MetricRecordListCreateView.as_view(), name="records-list"),
    path("metrics/<int:metric_id>/records/<int:record_id>/", MetricRecordDetailView.as_view(), name="record-detail"),
]
