import os
from celery import shared_task
from django.conf import settings
from app.core.models import Metric, MetricRecord


@shared_task
def create_fake_report():
    metrics_count = Metric.objects.count()
    records_count = MetricRecord.objects.count()

    report_content = f"Всего метрик: {metrics_count}\nВсего записей: {records_count}\n"

    file_path = os.path.join(settings.BASE_DIR, 'fake_report.txt')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    return f"fake_report обновлен!"