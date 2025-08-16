from rest_framework.serializers import ValidationError

class HabitRewardsValidators:
    """ Исключить одновременный выбор связанной привычки и указания вознаграждения. """

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, value):
        related_habits = value.get("related_habits")
        rewards = value.get("rewards")
        if related_habits is not None and rewards is not None:
            raise ValidationError("Нельзя одновременно указывать связанную привычку и вознаграждение.")
        if related_habits.is_pleasant is not True:
            raise ValidationError("В связанные привычки могут попадать только привычки с признаком приятной привычки.")

        return value


def periodicity_validators(value):
    """ Проверка на корректность периодичности. Периодичность должна быть целым числом от 1 до 7. """
    if value not in range(1, 8):
        raise ValidationError("Периодичность должна быть целым числом от 1 до 7.")
    return value


def time_to_complete_validators(value):
    """ Проверка на корректность времени выполнения. Время выполнения должно быть целым числом от 1 до 120. """
    if value not in range(1, 121):
        raise ValidationError("Время выполнения должно быть целым числом от 1 до 120.")
    return value


# def related_habits_validators(value):
#     """ Проверка на корректность связанных привычек. В связанные привычки могут попадать только привычки с признаком приятной привычки. """
#     if value is not None:
#         if not value.is_pleasant:
#             raise ValidationError("В связанные привычки могут попадать только привычки с признаком приятной привычки.")
#     return value


# def rewards_validators(value):
#     """ Исключить одновременный выбор связанной привычки и указания вознаграждения. """
#     if value is not None:
#         if value.related_habits:
#             raise ValidationError("Нельзя одновременно указывать связанную привычку и вознаграждение.")
#     return value


if __name__ == '__main__':
    print(periodicity_validators(1))
    print(periodicity_validators(7))
    # print(periodicity_validators(8))
    # print(periodicity_validators(0))
    # print(periodicity_validators(-1))
    # print(periodicity_validators(1.5))
    print(time_to_complete_validators(1))
    print(time_to_complete_validators(120))
    # print(time_to_complete_validators(1.1))
