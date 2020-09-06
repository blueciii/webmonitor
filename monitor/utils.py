from enum import Enum
import requests
import time
import re


class PatternState(Enum):
    NOT_FOUND = 0
    FOUND = 1
    NOT_CHECKED = 2


def time_me(function):
    def function_timer(*args, **kwargs):
        start = time.perf_counter()
        result = function(*args, **kwargs)
        duration = time.perf_counter() - start
        return result, duration
    return function_timer


@time_me
def check_website(url):
    try:
        response = requests.get(url, timeout=10)
        return (response, None)
    except requests.RequestException:
        return (None, 'RequestException')
    except requests.Timeout:
        return (None, 'Timeout')
    except requests.URLRequired:
        return (None, 'URLRequired')
    except requests.TooManyRedirects:
        return (None, 'TooManyRedirects')
    except requests.HTTPError:
        return (None, 'HTTPError')
    except requests.ConnectionError:
        return (None, 'ConnectionError')  
    except requests.FileModeWarning:
        return (None, 'FileModeWarning')
    except requests.ConnectTimeout:
        return (None, 'Connectiontimeout')
    except requests.ReadTimeout:
        return (None, 'ReadTimeout')


def check_sites(sites):
    status_list = []
    for site in sites:
        if 'url' in site.keys():
            pattern_found = PatternState.NOT_CHECKED
            # get site
            if 'url' in site.keys():
                url = site.get('url')
                (response, err), elapsed = check_website(url)                
                if (err):
                    status_code = None
                    history = None
                else:
                    status_code = response.status_code
                    history = [str(r.status_code) for r in response.history]
                    if len(history) > 0:
                        history = ','.join(history)
                    else:
                        history = None
                    if response.status_code == 200:
                        # check if we need to check the pattern
                        if 'pattern' in site.keys():
                            pattern_found = PatternState.NOT_FOUND
                            # check pattern
                            result = re.search(site.get('pattern'), response.text)
                            if result:
                                pattern_found = PatternState.FOUND
                status_list.append({
                    'site': site.get('name', url),
                    'httpcode': status_code,
                    'duration': elapsed,
                    'pattern': pattern_found.name,
                    'error': err,
                    'history': history
                })
    return status_list
