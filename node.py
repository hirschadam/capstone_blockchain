# Planning
# 	1 set up node listening on a socket
#		1.1 setup config
#			1.1.1 list of neighbors
#			1.1.2 default port
#	2 transmit data from one node to another

from socket import *
from threading import Thread 


class Node:
	
	def __init__(self, configFileName):
		
		self.peers_file = ''
		self.lport = 0
		self.sport = 0
		self.node_ip = ''
		self.name = ''
		f = open(configFileName)
		for row in f:
			line = row.split('=')
			if (line[0] == 'listeningPort'):
				self.lport = int(line[1].rstrip('\n'))
			if (line[0] == 'sendingPort'):
				self.sport = int(line[1].rstrip('\n'))
			if (line[0] == 'node_ip'):
				self.node_ip = line[1].rstrip('\n')
			if (line[0] == 'node_name'):
				self.name = line[1].rstrip('\n')
			if (line[0] == 'neighbors'):
				self.peers_file = line[1].rstrip('\n')

	def peer_info(self):

		f = open(self.peers_file)
		peers = []
		header = True
		for neighbor in f:
			if header:
				header = False
			else:
				peers.append(neighbor.split(','))
		return peers

	def get_sport(self):
		return self.sport

	def get_node_ip(self):
		return self.node_ip

	def get_name(self):
		return self.name

class Server(Thread):

	def __init__(self, node):
		
		Thread.__init__(self)
		self.port = node.get_sport()
		self.host = node.get_node_ip()
		self.name = node.get_name()
		self.bufsize = 1024
		self.addr = (self.host, self.port)

		self.socket = socket(AF_INET , SOCK_STREAM)
		self.socket.bind(self.addr)

	def run(self):
		
		self.socket.listen(5)
		while True:
			print 'Waiting for connection..'
			client, caddr = self.socket.accept()
			print 'Connected To',caddr

			peer_node = client.recv(self.bufsize)
			if peer_node:
				print(peer_node)
			else:
				continue


class Client(Thread):

	def __init__(self, node):
		
		Thread.__init__(self)
		self.port = node.get_sport()
		self.host = node.get_node_ip()
		self.name = node.get_name()
		self.bufsize = 1024
		self.addr = (self.host, self.port)
		self.listof_peers = node.peer_info()

		self.socket = socket(AF_INET , SOCK_STREAM)

	def run(self):

		invalid = True
		while invalid:
			try:
				invalid = False
				self.socket.connect(self.addr)
			except:
				invalid = True

		for i in range(len(self.listof_peers)):
			self.socket.send('Hey ' + self.listof_peers[i][1] + '\n')
	
		self.socket.close()
def main():
	
	filename = 'config.txt'
	node = Node(filename)
	server = Server(node)
	client = Client(node)

	server.start()
	client.start()

	server.join()


main()


## fuctions for peer managment
#def getInitialNeighbors(config):
#def listNeighbors():
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
	

