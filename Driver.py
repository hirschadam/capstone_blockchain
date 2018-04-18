from models import Input, Output, Transaction
from network import Node, Server
import time
import random

def createRewardTransaction(node):
    hash = 'BLOCK-REWARD'
    index = -1
    signature = "YOLO"
    input = Input(hash, index, signature)
    output = Output(5, str(node.pub_key.to_string()))
    transaction = Transaction([input], [output])
    print("Transaction: {} sent...".format(transaction.hash))
    node.sendTransaction(transaction)


if __name__ == '__main__':
	listOfConfigs = ['node1.txt', 'node2.txt', 'node3.txt', 'node4.txt']
	servers = []
	for conf in listOfConfigs:
		node = Node(conf)
		server = Server(node)
		servers.append(server)
		server.start()

	for i in range(10):
		time.sleep(5)
		randomIndex = random.randint(0, len(servers)-1)
		createRewardTransaction(servers[randomIndex].node)
		randomIndex = random.randint(0, len(servers)-1)
		servers[randomIndex].node.sendBlock()
		print("=====================================================")
		for server in servers:
			node = server.node
			print("Node {}'s Blockchain':\n{}\n".format(node.node_id, node.blockChain.__str__()))
		print("=====================================================")



	#TODO: Final lifecycle


	for s in servers:
		s.join()
