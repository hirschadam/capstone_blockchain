# Planning
# 	1 set up node listening on a socket
#		1.1 setup config
#			1.1.1 list of neighbors
#			1.1.2 default port
#	2 transmit data from one node to another

import socket


class Node:
	
	def __init__(self, nodeId, name, ip, listenPort, sendingPort):
		with open('config.txt') as f:
			lines = 
