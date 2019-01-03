import requests
re = requests.exceptions

IEX_API_ENDPOINT = 'https://api.iextrading.com/1.0'
REF_DATA_SYMBOLS = IEX_API_ENDPOINT + '/ref-data/symbols'
SM_BATCH_ENDPOINT = IEX_API_ENDPOINT + '/stock/market/batch'
SM_MOST_ACTIVE_LIST = IEX_API_ENDPOINT + '/stock/market/list/mostactive'
SM_SECTOR_PERFORMANCE_ENDPOINT = IEX_API_ENDPOINT + '/stock/market/sector-performance'

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

def get_batch(params, timeout):
    return request(SM_BATCH_ENDPOINT, timeout, params).json()

def get_most_active(timeout):
    return request(SM_MOST_ACTIVE_LIST ,timeout).json()

def get_sector_performance(timeout):
    return request(SM_SECTOR_PERFORMANCE_ENDPOINT, timeout).json()

def get_symbols(timeout):
    return request(REF_DATA_SYMBOLS ,timeout).json()
