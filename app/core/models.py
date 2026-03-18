from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField("название тега", max_length=50, unique=True)

    class Meta:
        verbose_name = "тэг"
        verbose_name_plural = "тэги"

    def __str__(self):
        return self.name


class Metric(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metrics')
    name = models.CharField("название метрики", max_length=255)
    description = models.TextField("описание", blank=True)

    class Meta:
        verbose_name = "метрика"
        verbose_name_plural = "метрики"

    def __str__(self):
        return self.name


class MetricRecord(models.Model):
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE, related_name='records')
    value = models.FloatField("Значение")
    timestamp = models.DateTimeField("Временная отметка", auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='records', blank=True)

    class Meta:
        verbose_name = "запись"
        verbose_name_plural = "записи"
        ordering = ['-timestamp']
