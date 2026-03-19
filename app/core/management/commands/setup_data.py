import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from app.core.models import Metric, MetricRecord, Tag

User = get_user_model()


class Command(BaseCommand):
    help = "Создает пользователей и начальные тестовые данные"

    def handle(self, *args: tuple, **kwargs: dict) -> None:
        admin_user, created = User.objects.get_or_create(username="admin")
        if created:
            admin_user.set_password("admin")
            admin_user.is_superuser = True
            admin_user.is_staff = True
            admin_user.save()

        test_user, created = User.objects.get_or_create(username="user")
        if created:
            test_user.set_password("user")
            test_user.save()

        tag_names = ["Тэг", "Круто!", "не круто"]
        tag_objs = []
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            tag_objs.append(tag)

        metric_names = ["Трафик", "Продажа", "Температура"]
        users = [admin_user, test_user]

        created_metric_objects = []

        for user in users:
            for m_name in metric_names:
                metric_obj, created = Metric.objects.get_or_create(
                    user=user, name=m_name, defaults={"description": f"Описание для {m_name}"}
                )
                created_metric_objects.append(metric_obj)

        for m_obj in created_metric_objects:
            if not m_obj.records.exists():
                for _ in range(5):
                    record = MetricRecord.objects.create(metric=m_obj, value=random.uniform(10.0, 100.0))  # noqa: S311
                    record.tags.add(random.choice(tag_objs))  # noqa: S311

        self.stdout.write(self.style.SUCCESS("Юзеры, тестовые метрики и записи созданы"))
