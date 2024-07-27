#!/usr/local/bin/python
import sys
import time
from stocks import Stocks


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print()


def main(args):
    if len(sys.argv) < 2:
        print(f"Require MarketCode Parameter <CN or US or HK>!\nUSAGE: python {__file__} MarketCode")
        sys.exit(2)

    market = str(args[1]).upper()

    param = {
        "CN": "sh_sz",
        "US": "us",
        "HK": "hk&is_delay=true"
    }
    if market not in param.keys():
        print("Unknown market code, please input the right code")
        sys.exit(2)

    _stocks = Stocks(market, param[market])

    _max = 35  # MAX=56
    size = 90
    print(f"acquire {market} market's stocks, please waiting for a while")
    print_progress_bar(0, _max, prefix='Progress:', suffix='Complete', length=50)
    for page in range(_max):
        print_progress_bar(page + 1, _max, prefix='Progress:', suffix='Complete', length=50)
        stock_list = _stocks.scrap(page + 1, size)
        _stocks.write2file(stock_list, page == 0)
        if _stocks.break_flag():
            break
        time.sleep(15)  # anti-robot

    print(f'Crawled {market} Stock Complete!')


if __name__ == "__main__":
    main(sys.argv)
