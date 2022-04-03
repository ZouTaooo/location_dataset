# -*- coding: utf-8 -*-

# This code shows an example of text translation from English to Simplified-Chinese.
# This code runs on Python 2.7.x and Python 3.x.
# You may install `requests` to run this code: pip install requests
# Please refer to `https://api.fanyi.baidu.com/doc/21` for complete api document

from pickle import TRUE
import string
from time import sleep
from pyparsing import empty
import requests
import random
import json
from hashlib import md5

import signal

# Set your own appid/appkey.
appid = ''
appkey = ''

# For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
from_lang = 'en'
to_lang = 'zh'

endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path

# query = 'Hello'


# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


def translate(query):
    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {
        'appid': appid,
        'q': query,
        'from': from_lang,
        'to': to_lang,
        'salt': salt,
        'sign': sign
    }

    # Send request
    while True:
        try:
            r = requests.post(url, params=payload, headers=headers, timeout=5)
            result = dict(r.json())
            if "error_code" in result.keys():
                print(result, payload)
                sleep(1)
            else:
                trans_result = result.get("trans_result", None)
                if trans_result is not None:
                    dst = trans_result[0].get('dst', None)
                    return dst
                return ""
        except Exception as e:
            sleep(1)
            print(e)


def ctrlc_handler(sig_num, frm):
    with open("./cities.json", "w+", encoding='utf-8') as new_f:
        json.dump(src_data, new_f, ensure_ascii=False, indent=4)
    exit(0)


signal.signal(signal.SIGINT, ctrlc_handler)

with open("./cities.json", 'r', encoding='utf-8') as f:
    src_data = json.loads(f.read())
    cities = src_data['cities']
    count = 0
    try:
        for city in cities:
            count += 1
            if 'zh_name' not in dict(city).keys():
                # if 'zh_name' not in city.keys():
                if city['name'] != '':
                    zh_name = translate(city['name'])
                    zh_name = zh_name.replace("酒店", "")
                    city['zh_name'] = zh_name
                    print("[%d/%d] [%s]==>[%s]" %
                          (count, len(cities), city['name'], zh_name))
                    sleep(1)
                else:
                    city['zh_name'] = city['name']
            else:
                city['zh_name'] = str(city['zh_name']).replace("酒店", "")
                print("[%d/%d] [%s]==>[%s]" %
                      (count, len(cities), city['name'], city['zh_name']))
    except Exception as e:
        print(e)
    finally:
        with open("./cities.json", "w+", encoding='utf-8') as new_f:
            json.dump(src_data, new_f, ensure_ascii=False, indent=4)
