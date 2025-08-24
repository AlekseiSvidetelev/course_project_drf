from django.conf import settings
from django.db import models


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Пользователь",
        help_text="Пользователь",
    )
    location = models.CharField(
        max_length=128,
        verbose_name="Место",
        help_text="Место",
    )
    start_time = models.TimeField(
        verbose_name="Время",
        help_text="Время",
    )
    action = models.CharField(
        max_length=255,
        verbose_name="Действие",
        help_text="Действие",
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
        help_text="Признак приятной привычки",
    )
    related_habits = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="Связанные привычки",
        help_text="Связанные привычки",
        null=True,
        blank=True,
    )
    periodicity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Периодичность",
        help_text="Периодичность от 1 до 7",
    )
    rewards = models.CharField(max_length=255, verbose_name="Награды", help_text="Награды", blank=True, null=True)
    time_to_complete = models.PositiveIntegerField(
        verbose_name="Время выполнения",
        help_text="Время выполнения от 0 до 120 секунд",
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Публичная привычка",
        help_text="Публичная привычка",
    )
    last_notification = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Последнее уведомление",
        help_text="Время последнего отправленного уведомления",
    )
    next_notification = models.DateTimeField(
        null=True, blank=True, verbose_name="Следующее уведомление", help_text="Когда отправить следующий раз"
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["-id"]

    def __str__(self):
        return f"Я буду {self.action} в {self.start_time} в {self.location}"
