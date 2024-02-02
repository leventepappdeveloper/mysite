from datetime import datetime
import pandas


class OptionUtils:

    @staticmethod
    def get_historical_data_by_date(historical_data: pandas.DataFrame,
                                    date: datetime):
        return historical_data.loc[historical_data['date'] == date.strftime('%Y-%m-%d')]

