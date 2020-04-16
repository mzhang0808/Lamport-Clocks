import threading
import queue
import socket
import sys
import time

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
                print(sys.argv[1] + " Print Clock:")
                for i in range(1,len(clocks)):
                    temp_split = clocks[i][0].split(',')
                    if temp_split[0] == 'l':
                        print(temp_split[1] + ', ' + str(clocks[i][1]))
                    elif temp_split[0] == 's':
                        print("Send '" + temp_split[1] + "' to " + temp_split[2] + ", " + str(clocks[i][1]))
                    else:
                        print("Receive '" + temp_split[1] + "', " + str(clocks[i][1]))

pid = sys.argv[1]
port = int(sys.argv[2])
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.1', port))
events = queue.Queue()
clocks = [('',0)]
threading.Thread(target = process).start()
threading.Thread(target = comm).start()
while True:
    time.sleep(0.01)
    e = input("Enter message: ")
    temp = e.split(',')
    events.put(e)
    

#l, wakeup
#s, foo, 3
#r, foo, 3, clock, pid