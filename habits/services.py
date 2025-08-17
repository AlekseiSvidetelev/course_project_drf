import requests
from django.utils import timezone
from datetime import timedelta
from config.settings import TELEGRAM_URL, TELEGRAM_TOKEN
from habits.models import Habit



def send_telegram_notification(chat_id, message):
    """Отправляет сообщение в телеграм"""
    params = {"chat_id": chat_id, "text": message}
    try:
        requests.get(f"{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage", params=params)
    except Exception as e:
        print(f"Во время отправки сообщения для {chat_id} произошла ошибка {e}")


def get_today_habits():
    """Возвращает привычки, для которых нужно отправить уведомление сегодня"""
    now = timezone.localtime()
    print(now)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    print(start_of_day)
    end_of_day = start_of_day + timedelta(days=1)
    print(end_of_day)
    return Habit.objects.filter(start_time__gte=start_of_day, start_time__lt=end_of_day)


if __name__ == "__main__":
    send_telegram_notification(1029764221, "test")
