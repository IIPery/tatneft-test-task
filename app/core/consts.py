from django.db import models


class SaleStatusConsts(models.TextChoices):
    PENDING = "pending", "В обработке"
    COMPLETED = "completed", "Завершено"
    CANCELLED = "canceled", "Отменено"
