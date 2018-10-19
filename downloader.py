import requests
from random import choice

def random_useragent():
    """ฟังก์ชั่นสำหรับ random user-agent ขึ้นมาใช้

    โดยจะอ่าน user-agent ขึ้นมาจากไฟล์ user-agents.txt แล้วจะเลือก random ขึ้นมา 1 ตัว

    Returns:
        dict: มี 5 key ได้แก่ User-Agent, Accept, Accept-Encoding, Connection, DNT

    """
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
    """ฟังก์ชั่นสำหรับ random proxy ขึ้นมาใช้

    โดยจะอ่าน proxy ขึ้นมาจากไฟล์ proxies.txt แล้วจะเลือก random ขึ้นมา 1 ตัว

    Returns:
        dict: key คือ protocol และ value คือ ip address:port

    """
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
    """ดาวน์โหลดเพจเว็บเพจที่ระบุ

    ดาวน์โหลดเว็บเพจโดยใช้ proxy และ user-agent จากการ random

    Args:
        url (string): url ของเว็บเพจที่ต้องการดาวน์โหลดซึ่งอยู่ในรูปที่ normalize แล้ว (เป็น absolute url และมี protocol) 
            เช่น http://www.example.com/test

    Returns:
        string: html ของเว็บเพจที่ดาวน์โหลดมา

    """
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