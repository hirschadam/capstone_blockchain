# Planning
from .block import Block
from .blockchain import Blockchain

from ecdsa import SigningKey, NIST384p
from socket import *
from threading import Thread
import sys
import time
import select
import pickle
import datetime
import random

class Node:

	def __init__(self, configFileName):

		self.peers_file = ''
		self.port_recv = 0
		self.sport = 0
		self.ip_addr = ''
		self.name = ''
		self.peer_list = []
		self.unspentTransactions = {}
		self.blockChain = Blockchain()
		index = self.blockChain.getBlock(self.blockChain.tailBlockHash).index
		prevHash = self.blockChain.tailBlockHash
		timestamp = datetime.datetime.utcnow().__str__()
		self.currBlock = Block(index, prevHash, timestamp)

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
		for peer in self.get_peer_list():
			self.sendData((3, transaction), peer)

	def signData(self, data):
		return self.priv_key.sign(data)

	def sendBlock(self):
		for peer in self.get_peer_list():
			self.sendData((4, self.currBlock), peer)
		self.blockChain.addBlock(self.currBlock)
		self.currBlock = Block(self.currBlock.index, self.currBlock.currHash, datetime.datetime.utcnow().__str__())

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
