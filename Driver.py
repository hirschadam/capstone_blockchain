from models import Input, Output, Transaction
from network import Node, Server
import threading
import time
import random

def runNode(server):
	server = Server(node)

	server.start()

	time.sleep(5)
	server.node.getNeihbors()

	server.join()

def createRewardTransaction(node):
    hash = 'BLOCK-REWARD'
    index = -1
    signature = "YOLO"
    input = Input(hash, index, signature)
    output = Output(5, str(node.pub_key.to_string()))
    transaction = Transaction([input], [output])
    print(transaction)
    node.sendTransaction(transaction)


if __name__ == '__main__':
	listOfConfigs = ['node1.txt', 'node2.txt', 'node3.txt', 'node4.txt']
	servers = []
	threads = []
	for conf in listOfConfigs:
		node = Node(conf)
		server = Server(node)
		servers.append(server)
		t = threading.Thread(target=runNode, args=(node,))
		t.start()
		threads.append(t)

	for i in range(50):
		time.sleep(5)
		randomIndex = random.randint(0, len(threads)-1)
		createRewardTransaction(servers[randomIndex].node)
	randomIndex = random.randint(0, len(threads)-1)
	servers[randomIndex].node.sendBlock()



	#TODO: Final lifecycle


	for t in threads:
		t.join()
