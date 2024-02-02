import datetime

from nakedPutOptionsTester.src.strategies.nakedPut.NakedPutBaseStrategy import NakedPutBaseStrategy
from nakedPutOptionsTester.src.client.IVolatilityClient import IVolatilityClient
from nakedPutOptionsTester.src.utils.ReportingUtils import ReportingUtils

if __name__ == '__main__':
    IVolatilityClient.authenticate()
    strategy = NakedPutBaseStrategy()
    backtest_data: dict = (
        strategy.backtest_strategy(
            stock_symbol='AAPL',
            start_date=datetime.datetime(2023, 1, 1),
            end_date=datetime.datetime(2023, 4, 1),
            dte=42,
            delta=-0.1,
            margin_requirement_rate=0.1
        )
    )

    k = ReportingUtils.generate_trade_log(backtest_data)
    #report = ReportingUtils.generate_performance_report(backtest_data, k)
    #ReportingUtils.create_performance_report(backtest_data, k, report)


