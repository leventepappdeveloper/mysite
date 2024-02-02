import pandas
import os
from datetime import datetime


class ReportingUtils:

    # Generates csv file
    @staticmethod
    def generate_trade_log(backtest_data: dict) -> pandas.DataFrame:
        df: pandas.DataFrame = pandas.DataFrame.from_dict(data=backtest_data['trade_history'],
                                                          orient='columns')
        trade_log: pandas.DataFrame = df.sort_values('entry_date')
        trade_log.sort_index()
        print(trade_log)
        return trade_log

    # Generates pdf file
    @staticmethod
    def generate_performance_report(backtest_data: dict, trade_log: pandas.DataFrame):
        additional_data = backtest_data['additional_data']

        total_net_profit: float = float(trade_log['profit'].sum()) * 100
        profit_factor: float = (-1) * float(trade_log['profit'][trade_log['profit'] > 0].sum() /
                                            trade_log['profit'][trade_log['profit'] <= 0].sum())
        percent_profitable: float = float(len(trade_log['profit'][trade_log['profit'] > 0]) /
                                          len(trade_log['profit'])) * 100
        average_trade_net_profit: float = float(total_net_profit / len(trade_log['profit'])) * 100
        maximum_drawdown: float = min(trade_log['profit']) * 100
        total_profit_percentage: float = float(total_net_profit / additional_data['maximum_margin_requirement']) * 100
        annualized_profit_percentage: float = float(365 * (total_profit_percentage /
                                                           (additional_data['end_date'] - additional_data[
                                                               'start_date']).days))

        return {
            'total_net_profit': total_net_profit,
            'maximum_margin_requirement': additional_data['maximum_margin_requirement'],
            'profit_factor': profit_factor,
            'percent_profitable': percent_profitable,
            'average_trade_net_profit': average_trade_net_profit,
            'maximum_draw_down': maximum_drawdown,
            'total_profit_percentage': total_profit_percentage,
            'annualized_profit_percentage': annualized_profit_percentage
        }

    @staticmethod
    def create_performance_report(backtest_data: dict, trade_log: pandas.DataFrame, performance: dict):
        time_stamp: datetime = datetime.now()
        output_path: str = os.path.abspath(os.getcwd()) + '/output/' + time_stamp.strftime('%Y-%m-%d')
        if not os.path.exists(output_path):
            os.mkdir(output_path)

        output_path = output_path + "/" + backtest_data['additional_data']['underlying_symbol']
        if not os.path.exists(output_path):
            os.mkdir(output_path)

        output_path = output_path + "/" + time_stamp.strftime('%Y-%m-%d') + "_" + time_stamp.strftime('%H.%M.%S')
        os.mkdir(output_path)

        trade_log.to_csv(output_path + "/" + "trade_log.csv")

        summary_file = open(output_path + "/summary.txt", "w")
        summary_file.write("Total Net Profit: " + str(performance['total_net_profit']) + "\n")
        summary_file.write("Maximum Margin Requirement: " + str(performance['maximum_margin_requirement']) + "\n")
        summary_file.write("Profit Factor: " + str(performance['profit_factor']) + "\n")
        summary_file.write("Percent Profitable: " + str(performance['percent_profitable']) + "\n")
        summary_file.write("Average Trade Net Profit: " + str(performance['average_trade_net_profit']) + "\n")
        summary_file.write("Maximum Draw-down: " + str(performance['maximum_draw_down']) + "\n")
        summary_file.write("Total Profit Percentage: " + str(performance['total_profit_percentage']) + "\n")
        summary_file.write("Annualized Profit Percentage: " + str(performance['annualized_profit_percentage']) + "\n")
        summary_file.close()
