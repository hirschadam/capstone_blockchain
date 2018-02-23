#!/usr/bin/env python3
import time
import hashlib

class Block:
    def __init__(self, index, prevHash, timestamp, data, currHash):
        self.index = index
        self.prevHash = prevHash
        self.timestamp = timestamp
        self.data = data
        self.currHash = currHash

    def getGenesisBlock():
        return Block(0, '0', 1518809761.5113006, "kek", "kek3st4nil4nd0000000000")

    blockchain = [getGenesisBlock()]

    def calculateHash(index, prevHash, timestamp, data):
        value = str(index) + str(prevHash) + str(timestamp) + str(data)
        sha = hashlib.sha256(value.encode('utf-8'))

        return str(sha.hexdigest())

    def calculateHashForBlock(block):
        return calculateHash(block.index, block.prevHash, block.timestamp, block.data)

    def getLatestBlock():
        return blockchain[len(blockchain-1)]

    def genNextBlock(blockData):
        prevBlock = getLatestBlock()
        nextIndex = prevBlock.index+1
        nextTimestamp = time.time()
        nextHash = calculateHash(nextIndex, prevBlock.currHash, nextTimestamp, blockData)
        return Block(nextIndex, prevBlock.currHash, nextTimestamp, nextHash)

    def isSameBlock(block1, block2):
        if block1.index != block2.index:
            return False
        elif block1.prevHash != block2.prevHash:
            return False
        elif block1.timestamp != block2.timestamp:
            return False
        elif block1.data != block2.data:
            return False
        elif block1.currHash != block2.currHash:
            return False
        return True

    def isValidNewBlock(newBlock, prevBlock):
        if prevBlock.index+1 != newBlock.index:
            print('Indices Do Not Match Up')
            return False
        elif prevBlock.currHash != newBlock.prevHash:
            print("Previous hash does not match")
            return False
        elif calculateHashForBlock(newBlock) != newBlock.hash:
            print("Invalid hashpointer")
            return False
        return True
            
    def isValidChain(chain)
        if not isSameBlock(chain[0], getGenesisBlock()):
            print('Genesis Block Incorrect')
            return False

        tempBlocks = [chain[0]]
        for i in range(1, len(chain)):
            if isValidNewBlock(chain[i], tempBlocks[i-1]):
                tempBlocks.append(chain[i])
            else:
                return False
        return True


