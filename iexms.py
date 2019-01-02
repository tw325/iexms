import requests
re = requests.exceptions

IEX_API_ENDPOINT = 'https://api.iextrading.com/1.0'
REF_DATA_SYMBOLS = IEX_API_ENDPOINT + '/ref-data/symbols'
STOCK_MARKET_BATCH_ENDPOINT = IEX_API_ENDPOINT + '/stock/market/batch'
STOCK_MARKET_SECTOR_PERFORMANCE_ENDPOINT = IEX_API_ENDPOINT + '/stock/market/sector-performance'

#TODO HANDLE ERROS AND TIMEOUTS
def request(url, timeout, *params):
    try:
        if len(params) == 0:
            return requests.get(url, timeout=timeout)
        elif len(params) == 1:
            return requests.get(url, params=params[0], timeout=timeout)
    except re.ConnectionError:
        print("ConnectionError")
    except re.HTTPError:
        print("HTTPError")
    except re.Timeout:
        print("Timeout")

def get_symbols(timeout):
    return request(REF_DATA_SYMBOLS ,timeout).json()

def get_sector_performance(timeout):
    return request(STOCK_MARKET_SECTOR_PERFORMANCE_ENDPOINT, timeout).json()

def get_batch(params, timeout):
    return request(STOCK_MARKET_BATCH_ENDPOINT, timeout, params).json()
