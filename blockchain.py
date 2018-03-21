#!/usr/bin/env python3

from block import Block

class Blockchain:
    def __init__(self):
        self.chain = {}
        self.genesisBlock = Block(0, '0', 1518809761.5113006, "kek")
        self.chain[genesisBlock.currHash] = self.genesisBlock
        self.tailBlockHash = genesisBlock.currHash

    def addBlock(self, block):
        if self.isValidBlock(block):
            self.chain[block.currHash] = block
            self.tailBlockHash = block.currHash
            return True
        return False

    def getBlock(self, hash):
        return self.chain[hash]

    def isValidBlock(self, block):
        prevBlock = self.getBlock(self.block.prevHash)
        if prevBlock.index+1 != block.index:
            print('Indices Do Not Match Up')
            return False
        elif prevBlock.currHash != block.prevHash:
            print("Previous hash does not match")
            return False
        elif block.calculateHash() != block.currHash:
            print("Invalid hashpointer")
            return False
        return block.isValid()

    def isValid(self):
        currBlock = self.getBlock(self.tailBlockHash)
        while currBlock != self.genesisBlock:
            if not self.isValidBlock(currBlock):
                return False
            currBlock = self.getBlock(currBlock.prevHash)
        return True

    
