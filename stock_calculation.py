import datetime


class Stock:
    def __init__(self, stock_symbol, type=None, last_dividend=None, fixed_dividend=None, par_value=None):
        self.stock_symbol = stock_symbol
        self.type = type
        self.last_dividend = last_dividend
        self.fixed_dividend = fixed_dividend
        self.par_value = par_value

    @property
    def get_stock_type(self):
        return self.type

    @property
    def get_stock_symbol(self):
        return self.stock_symbol

    @property
    def get_last_dividend(self):
        return self.last_dividend

    @property
    def get_fixed_dividend(self):
        return self.fixed_dividend

    @property
    def get_par_value(self):
        return self.par_value

    def calc_div_yield(self, price):
        '''Function Calculates the Dividend Yield of a given stock'''
        # check price input
        if price is None:
            raise ValueError("Price Input need to be provided")
        else:
            stock_type = self.get_stock_type
            if stock_type is None:
                raise ValueError("Stock Type Either Common or Preferred needs to be provided")
            else:
                if stock_type == "Common":
                    last_div = self.get_last_dividend
                    if last_div is None:
                        raise ValueError('Last dividend need to provided')
                    else:
                        return last_div / price
                elif stock_type == "Preferred":
                    fix_div = self.get_fixed_dividend
                    if fix_div is None:
                        raise ValueError("For Preferred Stock Fix Dividend needs to be provided")
                    else:
                        par_val = self.get_par_value
                        if par_val is None:
                            raise ValueError("Par Value needs to be provided")
                        else:
                            return (fix_div * par_val) / price
                else:
                    return "Stock Type provided by you needs to either be Common or Preferred"

    def calc_PE_Ratio(self, price):
        if price is None:
            raise ValueError("Price needs to be provided")
        else:
            try:
                dividend = self.get_last_dividend
                if dividend == 0:
                    return "P/E Ratio Cannot be calculated"
                else:
                    return price / dividend
            except Exception as e:
                raise e


import datetime as dt
from functools import reduce
import math


class Trade:
    stock_trade_list = {}

    def __init__(self, stock_name, quantity_of_share, indicator, trade_price):
        self.timestamp_trade = dt.datetime.now()
        self.stock_name = stock_name
        self.quantity_of_share = quantity_of_share
        self.indicator = indicator
        self.trade_price = trade_price
        if self.stock_name in Trade.stock_trade_list:
            value = Trade.stock_trade_list[self.stock_name]
            value.append((self.timestamp_trade,
                          self.quantity_of_share,
                          self.indicator,
                          self.trade_price))
            Trade.stock_trade_list[self.stock_name] = value
        else:
            Trade.stock_trade_list[self.stock_name] = [(self.timestamp_trade,
                                                        self.quantity_of_share,
                                                        self.indicator,
                                                        self.trade_price)]

    @staticmethod
    def get_stock_trading_list():
        return Trade.stock_trade_list

    @staticmethod
    def get_stock_trading_list_of_stock(stock_name):
        return Trade.stock_trade_list[stock_name]

    @staticmethod
    def find_time_difference(datetime_obj1, datetime_obj2):
        diff = datetime_obj1 - datetime_obj2
        return diff.total_seconds()

    @staticmethod
    def get_volume_weighted_stock_price(stock_name):
        current_time = datetime.datetime.now()
        time_frame = 15 * 60
        try:
            get_all_trades_of_stock = Trade.stock_trade_list[stock_name]
            trade_index = 0
            for trades in range(0, len(get_all_trades_of_stock)):
                get_time = get_all_trades_of_stock[trades][0]
                diff_in_sec = Trade.find_time_difference(datetime_obj1=current_time, datetime_obj2=get_time)
                if diff_in_sec < time_frame:
                    trade_index = trades
                    break
            weighted_stock_price_list = get_all_trades_of_stock[trade_index:]
            print(weighted_stock_price_list)
            sum_of_traded_price_quantity = 0
            sum_of_quantity = 0
            for w_stock_price in weighted_stock_price_list:
                traded_price = w_stock_price[3]
                quantity = w_stock_price[1]
                sum_of_traded_price_quantity += (traded_price * quantity)
                sum_of_quantity += quantity
            return sum_of_traded_price_quantity / sum_of_quantity
        except Exception as e:
            print(e)
            print("Some Issue while calculation of weighted stock price")

    @staticmethod
    def get_geometric_mean_of_stock(stock_name):
        get_stock_trades = Trade.stock_trade_list[stock_name]
        get_price = [trade[3] for trade in get_stock_trades]
        return math.sqrt(reduce(lambda x, y: x * y, get_price))

    @staticmethod
    def get_all_shared_index():
        get_all_stocks = list(Trade.stock_trade_list.keys())
        get_geo_mean_of_stocks = [Trade.get_geometric_mean_of_stock(stocks) for stocks in get_all_stocks]
        return math.sqrt(reduce(lambda x, y: x * y, get_geo_mean_of_stocks))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    '''
    Tea_Stock = Stock("TEA", type="Common", last_dividend=0, par_value=100)
    Pop_Stock = Stock("POP", type="Common", last_dividend=8, par_value=100)
    print(Tea_Stock.calc_div_yield(price=10))
    print(Tea_Stock.calc_PE_Ratio(price=10))
    print(Pop_Stock.calc_div_yield(price=8))
    print(Pop_Stock.calc_PE_Ratio(price=8))
    '''
    '''
    Trade_Tea = Trade("TEA", 40, "Buy", 10)
    Trade_Tea_1 = Trade("TEA", 10, "Sell", 8)
    Trade_Pop = Trade("POP", 20, "Sell", 8)
    Trade_Pop = Trade("POP", 20, "Buy", 4)
    print(Trade.get_stock_trading_list())
    print(Trade.get_stock_trading_list_of_stock("TEA"))
    print(Trade.get_volume_weighted_stock_price("POP"))
    print(Trade.get_all_shared_index())
    Testing Example i used
    '''
