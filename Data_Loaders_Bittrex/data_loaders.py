import requests
import pandas as pd
import json
from tqdm import tqdm


class DataLoader:

    def __init__(self):
        self.url_dict = {
            'tick_latest': 'https://bittrex.com/Api/v2.0/pub/market/GetLatestTick?marketName={}&tickInterval={}',
            'all_markets': 'https://bittrex.com/api/v1.1/public/getmarkets'
        }
        self.all_markets = self.get_all_markets()
        self.total_markets = len(self.all_markets)

    def get_result_from_url(self, url):
        """
        Helper function to get result from a url.
        :param url: URL of the API
        :return: Success (if the query was successful)(Boolean), Result dictionary
        """
        r = json.loads(requests.get(url).content)
        if r['success']:
            return r['success'], r['result']
        return r['success'], r['message']

    def get_all_markets(self):
        """
        Get a list of all available markets.
        :return: List of all available markets
        """
        success, result = self.get_result_from_url(self.url_dict['all_markets'])
        if success:
            all_currencies = [i['MarketName'] for i in result]
            return all_currencies
        return []

    def get_latest_tick_data(self, symbol, time_frame):
        """
        Get data of latest tick of the symbol
        :param symbol: Symbol to get data of
        :param time_frame: Timeframe for the ticker
        :return: Dictionary containing latest tick data for the symbol at timeframe
        """
        success, data = self.get_result_from_url(self.url_dict['tick_latest'].format(symbol, time_frame))
        return success, data[0]

    def get_all_ticks_data(self, start=0, end=None):
        """
        Get data for all ticks
        :return: Pandas DataFrame containing latest tick data for all tickers.
        """
        if end is None:
            end = len(self.all_markets)
        data = {
            'Symbol': [],
            'Volume': [],
            'Close': [],
            'Open': [],
            'High': [],
            'Low': [],
            'Timestamp': []
        }
        for i in tqdm(range(start, end)):
            sym = self.all_markets[i]
            try:
                sucess, temp_data = self.get_latest_tick_data(symbol=sym, time_frame='oneMin')
                if sucess is False:
                    print("Error for symbol {}".format(sym))
                    continue
                data['Symbol'].append(sym)
                data['Volume'].append(temp_data['V'])
                data['Close'].append(temp_data['C'])
                data['Open'].append(temp_data['O'])
                data['High'].append(temp_data['H'])
                data['Low'].append(temp_data['L'])
                data['Timestamp'].append(temp_data['T'])
            except Exception as e:
                print(e)
        final_data = pd.DataFrame(data=data).set_index('Timestamp')
        final_data.index = pd.to_datetime(final_data.index)
        return final_data

    def resample_data(self, data, timeperiod):
        """
        Resample OHLC data into different time periods
        :param data: DataFrame to be resampled
        :param timeperiod: timeperiod to be resampled in
        :return:
        """
        updated_data = {
            'Symbol': [],
            'Volume': [],
            'Close': [],
            'Open': [],
            'High': [],
            'Low': [],
            'Timestamp': []
        }
        for i in tqdm(range(len(self.all_markets))):
            try:
                temp_data = data[data['Symbol'] == self.all_markets[i]]
                ohlc_dict = {'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'}
                temp_data = temp_data.resample('{}T'.format(timeperiod), how=ohlc_dict).dropna(how='any')
                updated_data['Symbol'].extend([self.all_markets[i]] * temp_data.shape[0])
                updated_data['Volume'].extend(list(temp_data['Volume']))
                updated_data['Close'].extend(list(temp_data['Close']))
                updated_data['Open'].extend(list(temp_data['Open']))
                updated_data['High'].extend(list(temp_data['High']))
                updated_data['Low'].extend(list(temp_data['Low']))
                updated_data['Timestamp'].extend(list(temp_data.index))
            except Exception as e:
                print(e)
                continue
        updated_data = pd.DataFrame(updated_data).set_index('Timestamp')
        updated_data.index = pd.to_datetime(updated_data.index)
        return updated_data