import socket
import time
import random

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.1', 3000))

proc = {
    'p1': 3001,
    'p2': 3002,
    'p3': 3003
}

while True:
    cmd, addr = s.recvfrom(1024)
    cmd = cmd.decode('utf-8')
    temp = cmd.split(',')
    time.sleep(random.randint(1,6))
    #s, name, receiver, clock, pid
    s.sendto(cmd.encode('utf-8'), ('127.1', proc[temp[2]]))