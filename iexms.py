import requests
re = requests.exceptions

IEX_API_ENDPOINT = 'https://api.iextrading.com/1.0'
REF_DATA_SYMBOLS = IEX_API_ENDPOINT + '/ref-data/symbols'
STOCK_MARKET_BATCH_ENDPOINT = IEX_API_ENDPOINT + '/stock/market/batch'

def request_symbols(timeout):
    try:
        return requests.get(REF_DATA_SYMBOLS, timeout=timeout)
    except re.ConnectionError:
        # TODO:
        print("ConnectionError")
    except re.HTTPError:
        # TODO:
        print("HTTPError")
    except re.Timeout:
        # TODO:
        print("Timeout")

def request_url(url, params, timeout):
    try:
        return requests.get(url, params=params, timeout=timeout)
    except re.ConnectionError:
        # TODO:
        pass
    except re.HTTPError:
        # TODO:
        print("HTTPError")
    except re.Timeout:
        # TODO:
        pass

def get_symbols(timeout):
    return request_symbols(timeout).json()

def get_chart(params, timeout):
    return request_url(STOCK_MARKET_BATCH_ENDPOINT, params, timeout).json()
