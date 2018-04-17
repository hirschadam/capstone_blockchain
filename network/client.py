from .node import Node
from threading import Thread
import random
import time

class Client(Thread):
    def __init__(self, node):

        Thread.__init__(self)
        self.node = node
        self.peer_list = self.node.get_peer_list()
        self.port = self.node.get_sport()
        self.host = self.node.get_ip_addr()
        self.name = self.node.get_name()
        self.bufsize = 1024
        self.addr = (self.host, self.port)
        self.listof_peers = self.node.peer_info()
        self.node_id = self.node.get_id()

        self.socket = socket(AF_INET , SOCK_STREAM)

    def run(self):
        while True:
            mine_time = random.randint(30, 60)
            time.sleep(mine_time)
            self.node.sendBlock()
    
