from network import runNode
from models import Input, Output, Transaction
import threading


def createRandTransaction():


if __name__ == '__main__':
    listOfConfigs = ['node1.txt', 'node2.txt', 'node3.txt', 'node4.txt']
    threads = []
    for conf in listOfConfigs:
        t1 = threading.Thread(target=runNode, args=(conf,))
        t1.start()
        threads.append(t1)
    for t1 in threads:
        t1.join()
