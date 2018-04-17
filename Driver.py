from models import Input, Output, Transaction
from network import Node, Server, Client
import threading
import time
import random

def runNode(node):
	server = Server(node)
	client = Client(node)

	server.start()
	client.start()

	time.sleep(5)
	node.getNeihbors()

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
    nodes = []
    threads = []
    for conf in listOfConfigs:
        node = Node(conf)
        nodes.append(node)
        t1 = threading.Thread(target=runNode, args=(node,))
        t1.start()
        threads.append(t1)

    for i in range(50):
        time.sleep(5)
        randomIndex = random.randint(0, len(threads)-1)
        createRewardTransaction(nodes[randomIndex])


    for t1 in threads:
        t1.join()
