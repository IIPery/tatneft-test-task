import os
import pathlib

from celery import shared_task
from django.conf import settings

from app.core.models import Metric, MetricRecord


@shared_task
def create_fake_report() -> str:
    metrics_count = Metric.objects.count()
    records_count = MetricRecord.objects.count()

    report_content = f"Всего метрик: {metrics_count}\nВсего записей: {records_count}\n"

    file_path = os.path.join(settings.BASE_DIR, "fake_report.txt")

    pathlib.Path(file_path).write_text(report_content, encoding="utf-8")

    return "fake_report обновлен!"
