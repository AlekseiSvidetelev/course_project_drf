from datetime import timedelta

import requests
from django.utils import timezone

from config.settings import TELEGRAM_TOKEN, TELEGRAM_URL
from habits.models import Habit


def send_telegram_notification(chat_id, message):
    """Отправляет сообщение в телеграм и возвращает True при успехе."""
    params = {"chat_id": chat_id, "text": message}
    try:
        requests.get(f"{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage", params=params, timeout=5)
        return True
    except Exception as e:
        print(f"Ошибка при отправке: {e}")
        return False


def get_today_habits():
    """Привычки, которым нужно напомнить сегодня."""
    today_start = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    return Habit.objects.filter(next_notification__isnull=True) | Habit.objects.filter(next_notification__lt=today_end)
