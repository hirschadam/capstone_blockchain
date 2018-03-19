# Planning
# 	1 set up node listening on a socket
#		1.1 setup config
#			1.1.1 list of neighbors
#			1.1.2 default port
#	2 transmit data from one node to another

import socket


class Node:
	
	def __init__(self, nodeId, name, ip, listenPort, sendingPort):
		pass
	

def main():
	
	filename = 'config.txt'
	peers_file = ''
	f = open(filename)
	for row in f:
		line = row.split('=')
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

main()
	


