import datetime
import unittest
from nakedPutOptionsTester.src.utils.DateUtils import DateUtils


class Test(unittest.TestCase):

    def test_get_next_trading_day_with_monday(self):
        current_date = datetime.date(2023, 12, 11)
        expected_next = datetime.date(2023, 12, 12)
        actual_next = DateUtils.get_next_trading_day(current_date)
        self.assertEqual(expected_next, actual_next)

    def test_get_next_trading_day_with_tuesday(self):
        current_date = datetime.date(2023, 12, 12)
        expected_next = datetime.date(2023, 12, 13)
        actual_next = DateUtils.get_next_trading_day(current_date)
        self.assertEqual(expected_next, actual_next)

    def test_get_next_trading_day_with_wednesday(self):
        current_date = datetime.date(2023, 12, 13)
        expected_next = datetime.date(2023, 12, 14)
        actual_next = DateUtils.get_next_trading_day(current_date)
        self.assertEqual(expected_next, actual_next)

    def test_get_next_trading_day_with_thursday(self):
        current_date = datetime.date(2023, 12, 14)
        expected_next = datetime.date(2023, 12, 15)
        actual_next = DateUtils.get_next_trading_day(current_date)
        self.assertEqual(expected_next, actual_next)

    def test_get_next_trading_day_with_friday(self):
        current_date = datetime.date(2023, 12, 15)
        expected_next = datetime.date(2023, 12, 18)
        actual_next = DateUtils.get_next_trading_day(current_date)
        self.assertEqual(expected_next, actual_next)

    def test_get_next_trading_day_with_saturday(self):
        current_date = datetime.date(2023, 12, 16)
        expected_next = datetime.date(2023, 12, 18)
        actual_next = DateUtils.get_next_trading_day(current_date)
        self.assertEqual(expected_next, actual_next)

    def test_get_next_trading_day_with_sunday(self):
        current_date = datetime.date(2023, 12, 17)
        expected_next = datetime.date(2023, 12, 18)
        actual_next = DateUtils.get_next_trading_day(current_date)
        self.assertEqual(expected_next, actual_next)

    def test_get_all_trading_days_in_range_weekend(self):
        start_date = datetime.date(2023, 12, 16)
        end_date = datetime.date(2023, 12, 17)
        expected_trading_days = []
        actual_trading_days = DateUtils.get_all_trading_days_in_range(start_date, end_date)
        self.assertEqual(expected_trading_days, actual_trading_days)

    def test_get_all_trading_days_in_range_single_date(self):
        start_date = datetime.date(2023, 12, 11)
        end_date = datetime.date(2023, 12, 11)
        expected_trading_days = [datetime.date(2023, 12, 11)]
        actual_trading_days = DateUtils.get_all_trading_days_in_range(start_date, end_date)
        self.assertEqual(expected_trading_days, actual_trading_days)

    def test_get_all_trading_days_in_range_multiple_dates(self):
        start_date = datetime.date(2023, 12, 11)
        end_date = datetime.date(2023, 12, 19)
        expected_trading_days = [datetime.date(2023, 12, 11),
                                 datetime.date(2023, 12, 12),
                                 datetime.date(2023, 12, 13),
                                 datetime.date(2023, 12, 14),
                                 datetime.date(2023, 12, 15),
                                 datetime.date(2023, 12, 18),
                                 datetime.date(2023, 12, 19)]
        actual_trading_days = DateUtils.get_all_trading_days_in_range(start_date, end_date)
        self.assertEqual(expected_trading_days, actual_trading_days)
