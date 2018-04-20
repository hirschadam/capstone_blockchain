from models import Input, Output, Transaction
from network import Node, Server
import time
import random
import copy

def makeTransaction(node_send, node_rec, val):
    get_val = val
    transactions = copy.deepcopy(node_send.unSpentTransactions)
    inputs = []
    for hash in transactions:
        tr = transactions[hash]
        for index in range(len(tr.outputs)):
            output = tr.outputs[index]
            if output is not None:
                if output.pub_key == node_send.pub_key.to_string():
                    signature = node_send.priv_key.sign(hash.encode('utf-8'))
                    input = Input(hash, index, signature)
                    inputs.append(input)
                    get_val -= output.value
                    if get_val < 0.0:
                        break
    if get_val > 0.0:
        print("Not enough Coin to make Transaction...")
        return False

    outputs = []
    main_output = Output(node_rec.pub_key.to_string(), val)
    outputs.append(main_output)
    if get_val < 0.0:
        outputs.append(Output(node_send.pub_key.to_string(), 0.0-get_val))
    new_transaction = Transaction(inputs, outputs)
    node_send.sendTransaction(new_transaction)
    return True




def getNode(node_id, servers):
    for server in servers:
        if node_id == server.node.node_id:
            return server.node
    raise Exception("Node Not Found")

def createRewardTransaction(node):
    hash = 'BLOCK-REWARD'
    index = -1
    signature = "YOLO"
    input = Input(hash, index, signature)
    output = Output(node.pub_key.to_string(), 5.0)
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
                outputs = randNode.unSpentTransactions[input.hash].outputs
                output = outputs[input.index]
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
    listOfConfigs = ['node1.txt', 'node2.txt', 'node3.txt', 'node4.txt']
    servers = []
    for conf in listOfConfigs:
        node = Node(conf)
        server = Server(node)
        servers.append(server)
        server.start()

    for i in range(2):
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

    while True:
        line = input("Enter Transaction to Send> ")
        if line.strip() == "exit":
            sys.exit(0)
        args = line.split(" ")
        broke = False
        sendBlockFlag = 0
        try:
            node_send_id = args[0]
            node_rec_id = args[1]
            val = float(args[2])
            node_send = getNode(node_send_id, servers)
            node_rec = getNode(node_rec_id, servers)
            sendBlockFlag = int(args[3])
        except Exception as e:
            broke = True
        if not broke:
            broke &= makeTransaction(node_send, node_rec, val)
            print("Transaction Propagating....")
            time.sleep(10)
        else:
            print("Args: [node_send_id] [node_rec_id] [value] [sendBlock(1|0)]")
        if sendBlockFlag == 1 and not broke:
            node_send.sendBlock()
            time.sleep(12)
            printBalances(servers)


    for s in servers:
        s.join()
