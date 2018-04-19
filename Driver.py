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
    print("Transaction: {} being sent...".format(transaction.hash))
    node.sendTransaction(transaction)

def printBalances(servers):
    randNode = servers[0].node
    accounts = {}
    for hash in randNode.unSpentTransactions:
        transaction = randNode.unSpentTransactions[hash]
        for input in transaction.inputs:
            if input.hash != 'BLOCK-REWARD':
                outputs = randNode.blockChain.getTransaction(input.hash).outputs
                output = ouputs[input.index]
                if output is not None:
                    if output.pub_key not in accounts:
                        accounts[output.pub_key] = output.value
                    else:
                        accounts[output.pub_key] -= output.value
        for output in transaction.outputs:
            if output is not None:
                if output.pub_key not in accounts:
                    accounts[output.pub_key] = output.value
                else:
                    accounts[output.pub_key] += output.value
    print("\nAccount Summaries\n=====================================================")
    for account in accounts:
        node_id = 0
        for server in servers:
            if str(account) == str(server.node.pub_key.to_string()):
                node_id = server.node.node_id
        print("Node {} has a balance of {} Coins".format(node_id, accounts[account]))
    print("=====================================================")

if __name__ == '__main__':
    listOfConfigs = ['node1.txt', 'node2.txt', 'node3.txt', 'node4.txt', \
		'node5.txt', 'node6.txt', 'node7.txt', 'node8.txt', 'node9.txt', 'node10.txt']
    servers = []
    for conf in listOfConfigs:
        node = Node(conf)
        server = Server(node)
        servers.append(server)
        server.start()

    for i in range(5):
        time.sleep(5)
        randomIndex = random.randint(0, len(servers)-1)
        createRewardTransaction(servers[randomIndex].node)
        randomIndex = random.randint(0, len(servers)-1)
        servers[randomIndex].node.sendBlock()
        time.sleep(8)
        print("Blockchain Summaries\n=====================================================")
        for server in servers:
            node = server.node
            print("Node {}'s Blockchain':\n{}\n".format(node.node_id, node.blockChain.__str__()))
        print("=====================================================")
        printBalances(servers)

    #TODO: Final lifecycle


    for s in servers:
        s.join()
