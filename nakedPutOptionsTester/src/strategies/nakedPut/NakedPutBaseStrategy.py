"""
This strategy involves the following:
- sell 1 option on Friday (delta = -0.1), 42 DTE
- let it ride until 0 DTE, and sell at that point
"""
from datetime import datetime, timedelta
import pandas
from nakedPutOptionsTester.src.client.IVolatilityClient import IVolatilityClient
from nakedPutOptionsTester.src.utils.DateUtils import DateUtils


class NakedPutBaseStrategy:

    TRADE_LOG_COLUMN_NAMES = [
        'option_symbol',
        'entry_date',
        'expiration_date',
        'strike_price',
        'entry_price',
        'underlying_price_on_entry',
        'margin_requirement',
        'exit_date',
        'exit_price',
        'underlying_price_on_exit',
        'exit_type',
        'profit'
    ]

    def __init__(self):
        self.open_positions = {}
        self.historical_data_cache = {}
        self.positions_to_close = {}
        self.current_margin_requirement = 0
        self.maximum_margin_requirement = 0
        self.closed_positions = []
        self.trade_log_column_names = [
            'option_symbol',
            'entry_date',
            'expiration_date',
            'strike_price',
            'entry_price',
            'underlying_price_on_entry',
            'margin_requirement',
            'exit_date',
            'exit_price',
            'underlying_price_on_exit',
            'exit_type',
            'profit'
        ]

    def backtest_strategy(self,
                          stock_symbol: str,
                          start_date: datetime,
                          end_date: datetime,
                          dte: float,
                          delta: float,
                          margin_requirement_rate: float) -> dict:

        if stock_symbol == '':
            return {}

        if start_date > end_date:
            return {}

        if dte < 0:
            return {}

        if delta >= 0:
            return {}

        if margin_requirement_rate < 0 or margin_requirement_rate > 1:
            return {}

        self.__execute_strategy(stock_symbol,
                                start_date,
                                end_date,
                                dte,
                                delta,
                                margin_requirement_rate)

        return (
            {
                'column_names': self.trade_log_column_names,
                'trade_history': self.closed_positions,
                'additional_data': {
                    'underlying_symbol': stock_symbol,
                    'start_date': start_date,
                    'end_date': end_date,
                    'maximum_margin_requirement': self.maximum_margin_requirement
                }
            }
        )

    def __execute_strategy(self,
                           stock_symbol: str,
                           start_date: datetime,
                           end_date: datetime,
                           dte: float,
                           delta: float,
                           margin_requirement_rate: float):
        rolling_window: list = DateUtils.get_all_trading_days_in_range(start_date, end_date - timedelta(dte))
        for current_date in rolling_window:
            print(current_date)
            self.evaluate_active_positions(current_date)

            # Every Friday we open a new naked put position
            if current_date.weekday() == 4:
                self.open_new_position(stock_symbol, current_date, dte, delta, margin_requirement_rate)

    '''
    DOCUMENTATION
    '''
    def evaluate_active_positions(self,
                                  current_date: datetime):
        current_date_string: str = current_date.strftime('%Y-%m-%d')
        for option_symbol in self.open_positions:
            open_position: dict = self.open_positions[option_symbol]
            current_date_historical_data: pandas.DataFrame = (
                self.get_current_date_historical_data(
                    option_symbol,
                    current_date_string))
            if current_date_historical_data.empty:
                continue

            strike_price: float = float(open_position['strike_price'])
            entry_price: float = float(open_position['entry_price'])
            current_price: float = list(current_date_historical_data['bid'])[0]
            current_underlying_price: float = list(current_date_historical_data['Adjusted close'])[0]

            should_close_position: bool = False
            exit_type: str = ""

            if self.is_winning_position(entry_price, current_price):
                should_close_position = True
                exit_type = 'W'

            if self.is_losing_position(strike_price, current_underlying_price):
                should_close_position = True
                exit_type = 'L'

            if current_date_string == open_position['expiration_date']:
                should_close_position = True
                exit_type = 'E'

            if should_close_position:
                position_to_close: dict = self.build_closed_position(open_position,
                                                                     current_date_string,
                                                                     current_price,
                                                                     current_underlying_price,
                                                                     exit_type)
                self.positions_to_close[option_symbol] = position_to_close
        self.close_positions()

    def get_current_date_historical_data(self, option_symbol: str, current_date: str):
        option_symbol_data: pandas.DataFrame = self.historical_data_cache[option_symbol]
        return option_symbol_data.loc[option_symbol_data['date'] == current_date]

    @staticmethod
    def build_closed_position(open_position: dict,
                              exit_date: str,
                              exit_price: float,
                              underlying_price_on_exit: float,
                              exit_type: str):

        return {
            'option_symbol': open_position['option_symbol'],
            'entry_date': open_position['entry_date'],
            'expiration_date': open_position['expiration_date'],
            'strike_price': open_position['strike_price'],
            'entry_price': open_position['entry_price'],
            'underlying_price_on_entry': open_position['underlying_price_on_entry'],
            'margin_requirement': open_position['margin_requirement'],
            'exit_date': exit_date,
            'exit_price': exit_price,
            'underlying_price_on_exit': underlying_price_on_exit,
            'exit_type': exit_type,
            'profit': open_position['entry_price'] - exit_price
        }

    def close_positions(self):
        for position_to_close in self.positions_to_close:
            del self.open_positions[position_to_close]
            del self.historical_data_cache[position_to_close]
            self.current_margin_requirement -= self.positions_to_close[position_to_close]['margin_requirement']
            self.closed_positions.append(self.positions_to_close[position_to_close])

        self.positions_to_close = {}

    '''
    DOCUMENTATION
    '''
    def open_new_position(self,
                          stock_symbol: str,
                          current_date: datetime,
                          dte: float,
                          delta: float,
                          margin_requirement_rate: float):
        target_expiration_date: datetime = current_date + timedelta(dte)

        option_symbol, historical_data = IVolatilityClient.query_historical_options_data(
            stock_symbol,
            current_date,
            target_expiration_date,
            dte,
            delta,
            'P'
        )

        if option_symbol is None or historical_data is None:
            return

        self.historical_data_cache[option_symbol] = historical_data
        current_date_historical_data = self.get_current_date_historical_data(
            option_symbol,
            current_date.strftime('%Y-%m-%d'))

        strike_price: float = list(current_date_historical_data['strike'])[0]
        entry_price: float = list(current_date_historical_data['ask'])[0]
        underlying_price_on_entry: float = list(current_date_historical_data['Adjusted close'])[0]
        margin_requirement: float = margin_requirement_rate * 100 * underlying_price_on_entry

        open_position: dict = {
            'option_symbol': option_symbol,
            'entry_date': current_date.strftime('%Y-%m-%d'),
            'expiration_date': target_expiration_date.strftime('%Y-%m-%d'),
            'strike_price': strike_price,
            'entry_price': entry_price,
            'underlying_price_on_entry': underlying_price_on_entry,
            'margin_requirement': margin_requirement
        }

        self.current_margin_requirement += margin_requirement
        self.maximum_margin_requirement = max(self.maximum_margin_requirement, self.current_margin_requirement)
        self.open_positions[option_symbol] = open_position

    '''
     DOCUMENTATION
    '''
    def is_winning_position(self, entry_price: float, current_price: float):
        if 0.5 * entry_price >= current_price:
            return True
        return False

    '''
    DOCUMENTATION
    '''
    def is_losing_position(self, strike_price: float, current_underlying_price: float):
        if strike_price > current_underlying_price:
            return True
        return False
