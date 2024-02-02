import datetime
from typing import List


class DateUtils:
    @staticmethod
    def get_next_trading_day(date: datetime) -> datetime:
        date_day_id = date.weekday()

        if date_day_id >= 4:
            return date + datetime.timedelta(7 - date_day_id)

        return date + datetime.timedelta(1)

    @staticmethod
    def get_all_trading_days_in_range(start_date: datetime, end_date: datetime) -> List[datetime]:
        current_date = start_date
        weekdays = []
        while current_date <= end_date:
            if not current_date.weekday() in [5, 6]:
                weekdays.append(current_date)
            current_date = current_date + datetime.timedelta(1)
        return weekdays
