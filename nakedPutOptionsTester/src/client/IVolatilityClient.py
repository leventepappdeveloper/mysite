from datetime import datetime

import ivolatility as ivol
import pandas


class IVolatilityClient:

    @staticmethod
    def authenticate():
        credentials = open('credentials.txt', 'r')
        key_name: str = str(credentials.readline().strip('\n'))
        user_name: str = str(credentials.readline().strip('\n'))
        password: str = str(credentials.readline().strip('\n'))
        api_key = ivol.createApiKey(nameKey=key_name, username=user_name, password=password)
        ivol.setLoginParams(apiKey=api_key)

    @staticmethod
    def query_historical_options_data(stock_symbol: str,
                                      start_date: datetime,
                                      end_date: datetime,
                                      dte: float,
                                      delta: float,
                                      call_put: str):
        if stock_symbol is None or len(stock_symbol) == 0:
            return None, None

        if start_date is None or end_date is None or start_date > end_date:
            return None, None

        if dte is None or dte < 0:
            return None, None

        if delta is None or delta > 1 or delta < -1:
            return None, None

        if call_put not in ['P', 'C']:
            return None, None

        option_symbol: str = (
            IVolatilityClient.__query_nearest_option_symbol_by_delta(
                stock_symbol,
                start_date,
                dte,
                delta,
                call_put))
        if option_symbol is None or len(option_symbol) == 0:
            return None, None

        historical_data: pandas.DataFrame = IVolatilityClient.__query_historical_data_by_option_symbol(
            option_symbol,
            start_date,
            end_date)
        if historical_data is None or len(historical_data) == 0:
            return None, None

        return option_symbol, historical_data
    @staticmethod
    def __query_nearest_option_symbol_by_delta(stock_symbol: str,
                                               start_date: datetime,
                                               dte: float,
                                               delta: float,
                                               call_put: str):
        client = ivol.setMethod('/equities/eod/nearest-option-tickers')
        nearest_option_tickers: pandas.DataFrame = client(
            symbol=stock_symbol,
            startingDate=start_date.strftime('%Y-%m-%d'),
            dte=dte,
            delta=delta,
            callPut=call_put)

        if nearest_option_tickers.empty:
            return None

        return nearest_option_tickers['option_symbol'].iloc[-1]

    @staticmethod
    def __query_historical_data_by_option_symbol(option_symbol: str,
                                                 start_date: datetime,
                                                 end_date: datetime):
        client = ivol.setMethod('/equities/eod/single-stock-option')
        option_symbol_historical_data = client(symbol=option_symbol,
                                               from_=start_date.strftime('%Y-%m-%d'),
                                               to=end_date.strftime('%Y-%m-%d'))

        if option_symbol_historical_data.empty:
            return None

        return option_symbol_historical_data
