# Planning

from ecdsa import SigningKey, NIST384p
from socket import *
from threading import Thread
import sys
import time
import select
import pickle

class Node:

	def __init__(self, configFileName):

		self.peers_file = ''
		self.port_recv = 0
		self.sport = 0
		self.ip_addr = ''
		self.name = ''
		self.peer_list = []

		self.priv_key = SigningKey.generate(curve=NIST384p)
		self.pub_key = self.priv_key.get_verifying_key()

		f = open(configFileName)
		for row in f:
			line = row.split('=')
			if (line[0] == 'listeningPort'):
				self.port_recv = int(line[1].rstrip('\n'))
			if (line[0] == 'sendingPort'):
				self.sport = int(line[1].rstrip('\n'))
			if (line[0] == 'node_ip'):
				self.ip_addr = line[1].rstrip('\n')
			if (line[0] == 'node_id'):
				self.node_id = line[1].rstrip('\n')
			if (line[0] == 'node_name'):
				self.name = line[1].rstrip('\n')
			if (line[0] == 'neighbors'):
				self.peers_file = line[1].rstrip('\n')
		f.close()

	def peer_info(self):

		f = open(self.peers_file)
		peers = []
		header = True
		for neighbor in f:
			if header:
				header = False
			else:
				peers.append(neighbor.split(','))
		f.close()
		return peers

	def get_sport(self):
		return self.sport

	def get_ip_addr(self):
		return self.ip_addr

	def get_name(self):
		return self.name

	def get_id(self):
		return self.node_id

	def get_peer_list(self):
		return self.peer_list

	def sendTransaction(self, transaction):
		for peer in self.get_peer_list:
			self.sendData(transaction, peer)

	def sendData(self, data, recv):
		"""
		:param data: compsed of messageType and payload
		:param recv: node that recives the data
		"""
		print("sending data:", data, "To:", recv.name,"IP:", recv.ip_addr, "Port:", recv.port_recv,"From:", self.name, "IP:", self.ip_addr, "Port:", self.sport)
		s = socket(AF_INET, SOCK_STREAM)
		s.connect((recv.ip_addr, int(recv.port_recv)))
		s.send(pickle.dumps(data))

	def getNeihbors(self):
		peers = self.get_peer_list()
		newPeers = {}
		# Send neighbor request and node to reply to every peer currently in peer list
		for peer in peers:
			self.sendData((1,self),peer)

class Peer(object):

	def __init__(self, idx, name, ip_addr, port_send, port_recv):

		self.idx = idx
		self.name = name
		self.ip_addr = ip_addr
		self.port_send = port_send
		self.port_recv = port_recv

class Server(Thread):
	"""
		Recives messages from other nodes and acts accordingly
		messageType specifies what kind of data is contained in the payload
			1	Neighbor request
			2	Neighbor reply
			3	Transaction
			4	Block
			5	Blockchain request
			6	Blockchain reply
	"""

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
			print('Waiting for connection..')
			client, caddr = self.socket.accept()
			print('Connected To', caddr)

			serializedData = client.recv(self.bufsize)
			data = pickle.loads(serializedData)
			if data:
				print("Getting data",data)
				messageType, payload = data
				if messageType == 1:
					self.node.sendData((2, self.node.peer_list), payload)
				if messageType == 2:
					newPeers = set(self.node.peer_list)
					newPeers.update(payload)
					self.node.peer_list = list(newPeers)
			else:
				continue


class Client(Thread):

	def __init__(self, node):

		Thread.__init__(self)
		self.peer_list = node.get_peer_list()
		self.port = node.get_sport()
		self.host = node.get_ip_addr()
		self.name = node.get_name()
		self.bufsize = 1024
		self.addr = (self.host, self.port)
		self.listof_peers = node.peer_info()
		self.node_id = node.get_id()

		self.socket = socket(AF_INET , SOCK_STREAM)

	def run(self):

		MAX_CONNECTION_ATTEMPTS = 3
		SECONDS_BETWEEN_CONNECTION_ATTEMPTS = 3
		for i in range(len(self.listof_peers)):
			peer = self.listof_peers[i]
			if self.node_id != peer[0]:
				peer_addr = (peer[2],int(peer[4]))
				attempts = 0
				while attempts < MAX_CONNECTION_ATTEMPTS:
					try:
						print("connecting to", peer_addr)
						self.socket.connect(peer_addr)
						self.socket.send(pickle.dumps((0,'Hey ' + peer[1] + " I'm " + self.name + '\n')))
						attempts = MAX_CONNECTION_ATTEMPTS
						print("Said hey to", peer[1], peer[2], peer[3], peer[4])
						peer_object = Peer(peer[0], peer[1], peer[2], peer[3], peer[4])
						self.peer_list.append(peer_object)

					except:
						print("Error sending to peer", peer[1] + ".","retry number", attempts)
						attempts += 1
						if attempts == MAX_CONNECTION_ATTEMPTS:
							print("Giving up on", peer[1], ":'(")
						time.sleep(SECONDS_BETWEEN_CONNECTION_ATTEMPTS)
				self.socket.close()

def runNode(filename):
	node = Node(filename)
	server = Server(node)
	client = Client(node)

	server.start()
	client.start()

	time.sleep(5)
	node.getNeihbors()

	server.join()

def main():
	print("Building node from", sys.argv[1])
	filename = sys.argv[1]
	runNode(filename)


if __name__ == '__main__':
	main()

## fuctions for peer managment
#def getInitialNeighbors(config):
#def addNeighbor(nodeId, name, ip_addr, port_send, port_recv):
#def blacklistNeighbor(nodeId):
## fuctions for sending and reciving transactions and blocks
#def sendTransaction():
#def verifyTransaction():
#def sendBlock():
#def verifyBlock():
##functions for managing the blockchain
#def listBlocks():
#def addToBlockchain():
#def getNewestBlock():
