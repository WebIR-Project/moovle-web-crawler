import requests
from random import choice

class Downloader:
    def __init__(self, use_proxies=False):
        self.use_proxies = use_proxies

    def random_useragent(self):
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

    def random_proxy(self):
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

    def get_page(self, url) :
        """ดาวน์โหลดเพจเว็บเพจที่ระบุ

        ดาวน์โหลดเว็บเพจโดยใช้ proxy และ user-agent จากการ random

        Args:
            url (string): url ของเว็บเพจที่ต้องการดาวน์โหลดซึ่งอยู่ในรูปที่ normalize แล้ว (เป็น absolute url และมี protocol) 
                เช่น http://www.example.com/test

        Returns:
            string: html ของเว็บเพจที่ดาวน์โหลดมา

        """
        try :
            if self.use_proxies:
                r = requests.get(url, headers=self.random_useragent(), proxies=self.random_proxy(), timeout=3)
            else:
                r = requests.get(url, timeout=3)
            if r.status_code == 404 or r.status_code == 403:
                raise PageNotFound(f'{url} does not exist.')
            html = r.text
            return html
        except requests.exceptions.ProxyError:
            raise NetworkError('proxy error.')
        except requests.exceptions.ConnectTimeout:
            raise NetworkError('connection timeout.')
        except requests.exceptions.ReadTimeout:
            raise NetworkError('read timed out.')
        except requests.exceptions.ConnectionError:
            raise NetworkError('connection error')

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class PageNotFound(Error):
    def __init__(self, message):
        self.message = message

class NetworkError(Error):
    def __init__(self, message):
        self.message = message