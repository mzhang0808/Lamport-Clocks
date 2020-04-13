import threading
import queue
import socket
import sys

def comm():
    global events
    while True:
        cmd, addr = s.recvfrom(1024)
        cmd = cmd.decode('utf-8')
        temp = "r" + cmd[1:]
        events.put(temp)
        
def process():
    global events
    global clocks
    while True:
        while events.not_empty:
            event = events.get()
            temp = event.split(',')
            if temp[0] == 'l':
                clocks.append((event, clocks[-1][1]+1))
            elif temp[0] == 's':
                addr = ('127.1', 3000)
                clocks.append((event, clocks[-1][1]+1))
                event = event + "," + str(clocks[-1][1]) + "," + pid
                s.sendto(event.encode('utf-8'), addr)
            elif temp[0] == 'r':
                clocks.append((temp[0] + "," + temp[1], max(clocks[-1][1], int(temp[-2])) + 1))
            else:
                print(clocks[1:])
            

pid = sys.argv[1]
port = int(sys.argv[2])
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.1', port))
events = queue.Queue()
clocks = [('',0)]
threading.Thread(target = process).start()
threading.Thread(target = comm).start()
while True:
    e = input()
    temp = e.split(',')
    events.put(e)
    

#l, wakeup
#s, foo, 3
#r, foo, 3, clock, pid