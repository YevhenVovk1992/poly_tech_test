from datetime import datetime
from django.core import exceptions
from django.utils import timezone


class DateValidator:

    @staticmethod
    def timestamp_validator(time_data: datetime) -> datetime:
        time2 = timezone.now()
        if time2 > time_data:
            raise exceptions.ValidationError('Date must not be in past time')
        return time_data

