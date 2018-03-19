# Planning
# 	1 set up node listening on a socket
#		1.1 setup config
#			1.1.1 list of neighbors
#			1.1.2 default port
#	2 transmit data from one node to another

import socket


class Node:
	
	def __init__(self, configFileName):
		peers_file = ''
		lport = 0
		sport = 0
		node_ip = ''
		name = ''
		f = open(configFileName)
		for row in f:
			line = row.split('=')
			if (line[0] == 'listeningPort'):
				lport = line[1].rstrip('\n')
			if (line[0] == 'sendingPort'):
				sport = line[1].rstrip('\n')
			if (line[0] == 'node_ip'):
					node_ip = line[1].rstrip('\n')
			if (line[0] == 'node_name'):
				name = line[1].rstrip('\n')
			if (line[0] == 'neighbors'):
				peers_file = line[1].rstrip('\n')
		
		f = open(peers_file)
		header = True
		for neighbor in f:
			if header:
				header = False
			else:
				(idx, name, ip_addr, port_send, port_recv) = neighbor.split(',')
				print(idx,name)
	
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
	

def main():
	
	filename = 'config.txt'
	node = Node(filename)
	

main()
