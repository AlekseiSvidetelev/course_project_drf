from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.services import get_today_habits, send_telegram_notification


@shared_task
def run_daily_scan():
    """Запускается в 00:00 и ставит уведомления на сегодня."""
    for habit in get_today_habits():
        send_notification.apply_async(
            args=[habit.id],
            eta=timezone.localtime().replace(
                hour=habit.start_time.hour, minute=habit.start_time.minute, second=0, microsecond=0
            ),
        )


@shared_task
def send_notification(habit_id):
    habit = Habit.objects.select_related("user").get(id=habit_id)
    user = habit.user
    if not user or not user.tg_chat_id:
        print(f"На привычке {habit.id} не найден пользователь или не указан чат ID в телеграме")
        return

    message = (
        f"*Напоминание о привычке!*\n"
        f"Действие: {habit.action}\n"
        f"Место: {habit.location}\n"
        f"Время выполнения: {habit.time_to_complete} секунд\n"
        f"Вознаграждение: {habit.rewards or habit.related_habits or 'нет'}\n"
        f"Периодичность дней: {habit.periodicity}."
    )

    if send_telegram_notification(user.tg_chat_id, message):
        now = timezone.now()
        habit.last_notification = now
        habit.next_notification = now + timedelta(days=habit.periodicity)
        habit.save()
