from .node import Node
from models.block import Block
from models.blockchain import Blockchain
from socket import *
import random
import pickle
import time
from threading import Thread

# Message types for communication between nodes
REQUEST_NEIGHBORS = 1
REPLY_NEIGHBORS = 2
TRANSACTION = 3
BLOCK = 4
REQUEST_BLOCKCHAIN = 5
REPLY_BLOCKCHAIN = 6

class Server(Thread):

	def __init__(self, node):

		Thread.__init__(self)
		self.port = node.port_recv
		self.host = node.get_ip_addr()
		self.name = node.get_name()
		self.bufsize = 1024
		self.addr = (self.host, self.port)
		self.node_id = node.get_id()
		self.node = node

		self.socket = socket(AF_INET , SOCK_STREAM)
		self.socket.bind(self.addr)

	def run(self):
		self.socket.listen(5)           
		while True:
			print("Node " + self.node_id +': waiting for connection..')
			client, caddr = self.socket.accept()
			print('Connected To', caddr)

			serializedData = client.recv(self.bufsize)
			data = pickle.loads(serializedData)
			if data:
				messageType, payload = data
				if messageType == REQUEST_NEIGHBORS:
					self.node.sendData((REPLY_NEIGHBORS, self.node.peer_list), payload)
				if messageType == REPLY_NEIGHBORS:
					newPeers = set(self.node.peer_list)
					newPeers.update(payload)
					self.node.peer_list = list(newPeers)
				if messageType == TRANSACTION:
					self.node.unspentTransactions[payload.hash] = payload
					self.node.currBlock.addTransaction(payload, self.node.unspentTransactions)
				if messageType == BLOCK:
					if self.blockChain.isValidBlock(payload):
						for peer in self.node.get_peer_list():
							self.sendData((4, payload), peer)
							self.blockChain.addBlock(payload)
						self.currBlock = Block(payload.index, payload.currHash, datetime.datetime.utcnow().__str__())

					client.close()
			else:
				client.close()
				continue


