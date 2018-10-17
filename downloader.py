import requests
from random import choice

def random_useragent():
    UAS = []
    HEADERS = {
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'close',
                'DNT': '1'
            }
    #if you want more user agent ,just google and add !
    with open('./user-agents.txt') as f:
        UAS = list(set(f.read().split('\n')))
    HEADERS['User-Agent'] = choice(UAS)
    return HEADERS

def random_proxy():
    proxy_list = []
    with open('./proxies.txt') as f:
        proxys = f.read().split('\n')
    for i in proxys:
        if len(i) > 5:
            if i[:4] != 'http':
                proxy_list.append('http://'+i.split('\n')[0])
            else:
                proxy_list.append(i.split('\n')[0])
    proxy_list = list(set(proxy_list))
    selected_proxy = choice(proxy_list)
    return {selected_proxy.split('://')[0]: selected_proxy.split('://')[1]}

def get_page(url) :
    try :
        r = requests.get(url, headers=random_useragent(), proxies=random_proxy(), timeout=3)
        html = r.text
        if r.status_code == 404:
            print(f'404: {url}')
            html = None
        return html
    except requests.exceptions.ProxyError:
        print('proxy error')
    except requests.exceptions.ConnectTimeout:
        print('connection timeout')
    except Exception as e:
        print(f'getting page error: {url}')
        print(e)
        raise