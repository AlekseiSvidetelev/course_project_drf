from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from habits.models import Habit
from habits.services import get_today_habits, send_telegram_notification


@shared_task
def run_daily_scan():
    """Ежедневное сканирование и планирование уведомлений"""
    today_habits = get_today_habits()
    for habit in today_habits:
        notification_time = timezone.localtime().replace(
            hour=habit.start_time.hour,
            minute=habit.start_time.minute,
            second=0,
            microsecond=0
        )
        if notification_time < timezone.localtime():
            notification_time += timedelta(days=1)
        send_notification.apply_async(
            args=[habit.id],
            eta=notification_time
        )
        print(f"Запланировано уведомление для {habit.id} на {notification_time}")


@shared_task
def send_notification(habit_id):
    """Отправляет уведомление для конкретной привычки"""
    try:
        habit = Habit.objects.get(id=habit_id)
    except Habit.DoesNotExist:
        return

    if not habit.user.tg_chat_id:
        print(f"У пользователя {habit.user} не указан Telegram Chat ID")
        return
    reward = habit.rewards if habit.rewards else (
        habit.related_habits.action if habit.related_habits else "нет"
    )
    message = (
        f"*Напоминание о привычке!*\n"
        f"Действие: {habit.action}\n"
        f"Место: {habit.location}\n"
        f"Время выполнения: {habit.time_to_complete} секунд\n"
        f"Вознаграждение: {habit.rewards if habit.rewards else habit.related_habits}\n"
        f"Периодичность: раз в {habit.periodicity} дней"
    )
    if send_telegram_notification(habit.user.tg_chat_id, message):
        habit.last_notification = timezone.now()
        habit.save()
