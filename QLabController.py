from socket import *
import socket
import threading
from _thread import *
import sys
import time


t_lock=threading.Condition()

class QLabController:

    def __init__(self, ip_qlab, port, ip_device):
        self.ip_qlab = ip_qlab
        self.port = port
        self.address = (ip_qlab, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recv_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        timeout = 0
        start_time = time.time()
        while(timeout < 60):
            try:
                self.recv_socket.bind((ip_device, 53000))
                break
            except:
                continue
            timeout = time.time() - start_time
        self.recv_msg = ""
  

        Central = threading.Thread(target=self.checkIncoming)
        Central.daemon = True
        Central.start()

    # Sends given cue to QLab
    def cue(self, message):
        self.socket.sendto(message, self.address)

    # Resets QLab workspace by sending sequence of commands to initialise as necessary

    
    def checkIncoming(self):
        global t_lock
        print("Starting threading...")
        while 1:
            data, addr = self.recv_socket.recvfrom(1024)
            data = data.decode()

            if not data: 
                continue
            with t_lock:
                self.recv_msg = data
                print("Received message: %s" % data)
                t_lock.notify()
        

    def __del__(self):
      self.socket.close()
    