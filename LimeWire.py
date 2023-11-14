import base64
import json
import pprint
import random
import re
import ssl
import time

import requests
import cloudscraper

import capmonster_python






def random_user_agent():
    browser_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{0}.{1}.{2} Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_{2}_{3}) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{1}.{2}) Gecko/20100101 Firefox/{1}.{2}',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{0}.{1}.{2} Edge/{3}.{4}.{5}'
    ]

    chrome_version = random.randint(70, 108)
    firefox_version = random.randint(70, 108)
    safari_version = random.randint(605, 610)
    edge_version = random.randint(15, 99)

    chrome_build = random.randint(1000, 9999)
    firefox_build = random.randint(1, 100)
    safari_build = random.randint(1, 50)
    edge_build = random.randint(1000, 9999)

    browser_choice = random.choice(browser_list)
    user_agent = browser_choice.format(chrome_version, firefox_version, safari_version, edge_version, chrome_build, firefox_build, safari_build, edge_build)

    return user_agent


class LimeWire:

    def __init__(self, ref, mail, proxy):
        self.mail = mail
        self.defaultProxy = proxy
        self.ref = ref

        proxy = proxy.split(':')
        proxy = f'http://{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}'

        self.proxy = {'http': proxy,
                           'https': proxy}
        print(self.proxy)

        self.session = self._make_scraper()
        self.session.proxies = self.proxy
        self.session.user_agent = random_user_agent()
        adapter = requests.adapters.HTTPAdapter(max_retries=5)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def main(self):

        with self.session.post(f'https://api.kickofflabs.com/v1/171250/subscribe?email={self.mail}&social_id={self.ref}', timeout=10) as response:
            # print(response.text)
            if response.json()['waitlisted'] == True:
                return 'Successfully Registered'
            else:
                return 'Error'


    def _make_scraper(self):
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers(
            "ECDH-RSA-NULL-SHA:ECDH-RSA-RC4-SHA:ECDH-RSA-DES-CBC3-SHA:ECDH-RSA-AES128-SHA:ECDH-RSA-AES256-SHA:"
            "ECDH-ECDSA-NULL-SHA:ECDH-ECDSA-RC4-SHA:ECDH-ECDSA-DES-CBC3-SHA:ECDH-ECDSA-AES128-SHA:"
            "ECDH-ECDSA-AES256-SHA:ECDHE-RSA-NULL-SHA:ECDHE-RSA-RC4-SHA:ECDHE-RSA-DES-CBC3-SHA:ECDHE-RSA-AES128-SHA:"
            "ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-NULL-SHA:ECDHE-ECDSA-RC4-SHA:ECDHE-ECDSA-DES-CBC3-SHA:"
            "ECDHE-ECDSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA:AECDH-NULL-SHA:AECDH-RC4-SHA:AECDH-DES-CBC3-SHA:"
            "AECDH-AES128-SHA:AECDH-AES256-SHA"
        )
        ssl_context.set_ecdh_curve("prime256v1")
        ssl_context.options |= (ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1_3 | ssl.OP_NO_TLSv1)
        ssl_context.check_hostname = False

        return cloudscraper.create_scraper(
            debug=False,
            ssl_context=ssl_context
        )

if __name__ == '__main__':

    Emails=[]
    Proxies=[]
    ref=''
    intervalMax=0
    intervalMin=0

    with open('Data/Config.txt', 'r') as file:
        for i in file:
            if 'REF_CODE' in i:
                ref = i.split('REF_CODE=')[-1].strip('\n')
            elif 'INTERVAL' in i:
                intervalMax = float(i.split('INTERVAL=')[-1].strip('\n').split('-')[1])
                intervalMin = float(i.split('INTERVAL=')[-1].strip('\n').split('-')[0])

    with open('Data/Email.txt') as file:
        for i in file:
            Emails.append(i.split(':')[0].strip('\n'))

    with open('Data/Proxy.txt') as file:
        for i in file:
            Proxies.append(i.strip('\n'))

    if len(Emails) != len(Proxies):
        input('Неравномерное распределение данных в файлах')
        exit(1)

    if intervalMin > intervalMax:
        input('Интервал задержки прописан в неправильном формате')
        exit(1)

    if len(ref) != 6:
        input('Реферальный код прописан в неверном формате')
        exit(1)


    for i in range(len(Emails)):

        Acc = LimeWire(ref=ref,
                       mail=Emails[i],
                       proxy=Proxies[i]).main()

        print(i, f'- {Acc}')

        time.sleep(random.randint(int(intervalMin), int(intervalMax)))



