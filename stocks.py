import pandas as pd
import requests


class Stocks:
    keys_to_keep = [
        'symbol', 'name', 'market_capital', 'float_market_capital', 'total_shares',
        'current', 'pb_ttm', 'pb', 'pe_ttm', 'eps', 'pcf', 'ps',
        'type', 'dividend_yield', 'issue_date_ts'
    ]

    is_break = False

    def __init__(self, market, m_type):
        self.market = market
        self.m_type = m_type
        self.csv_file = f"stock-of-{market}-capital.csv"
        self.__read_cookie()

    def break_flag(self):
        return self.is_break

    def __read_cookie(self):
        try:
            with open(".cookie", 'r') as file:
                self.cookie = file.read()
        except:
            print("no .cookie found")

    # 雪球行情
    def scrap(self, page=1, size=90):
        host = 'https://stock.xueqiu.com'
        url = f'{host}/v5/stock/screener/quote/list.json?page={page}&size={size}&order=desc&order_by=market_capital&market={self.market}&type={self.m_type}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive',
            'Origin': 'https://xueqiu.com',
            'Referer': 'https://xueqiu.com',
            'Priority': 'u=1, i',
            'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': 'Windows',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'same-site',
            'Sec-Fetch-Site': 'cors',
            'Cookie': self.cookie
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            stock_list = data["data"]["list"]
            return stock_list
        else:
            return []

    # private method
    def __append_json_to_csv(self, data_of_threshold, need_header):
        columns = self.keys_to_keep
        json_df = pd.DataFrame(data_of_threshold, columns=columns)
        json_df.to_csv(self.csv_file, mode='a', header=need_header, index=False)

    def write2file(self, stock_list, need_header=False):
        threshold = 1 if self.market == 'US' else 6
        data_of_threshold = []
        for stock in stock_list:
            market_capital = stock["market_capital"]
            if market_capital > threshold * 1000000000:  # 只考虑10亿美金市值以上的股票
                filtered_stock = {key: stock.get(key, -1) for key in self.keys_to_keep if key in stock}
                data_of_threshold.append(filtered_stock)
            else:
                self.is_break = True
                print("under threshold, exit")
                break
        if len(data_of_threshold) > 0:
            self.__append_json_to_csv(data_of_threshold, need_header)
