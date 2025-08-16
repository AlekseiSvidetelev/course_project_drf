from rest_framework.fields import IntegerField, CharField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from habits.models import Habit
from habits.validators import periodicity_validators, time_to_complete_validators,  \
    HabitRewardsValidators


class HabitSerializer(ModelSerializer):
    periodicity = IntegerField(validators=[periodicity_validators],)
    time_to_complete = IntegerField(validators=[time_to_complete_validators],)



    class Meta:
        model = Habit
        fields = "__all__"
        validators = [HabitRewardsValidators(fields="__all__")]
