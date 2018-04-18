#!/usr/bin/env python3

from .block import Block

class Blockchain:
    def __init__(self):
        """
        Constructor for Blockchain
        """
        self.chain = {}
        self.genesisBlock = Block(0, 'kek', 1518809761.5113006)
        self.chain[self.genesisBlock.currHash] = self.genesisBlock
        self.tailBlockHash = self.genesisBlock.currHash


    def addBlock(self, block):
        """
        Add Block to Blockchain

        @param block - Block to be added to the chain

        @return Boolean - True if block was added, False otherwise
        """
        if self.isValidBlock(block):
            self.chain[block.currHash] = block
            self.tailBlockHash = block.currHash
            return True
        return False

    def getBlock(self, hash):
        """
        Get Block from Blockchain

        @param hash - Hash of Block to get

        @return Block - The Block in question, or None
        """
        if hash in self.chain:
            return self.chain[hash]
        return None

    def isValidBlock(self, block):
        """
        Checks if Block is Valid

        @param block - Block to be checked

        @return Boolean - True if block is valid, False otherwise
        """

        prevBlock = self.getBlock(self.tailBlockHash)
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
        """
        Check if Blockchain is Valid

        @return Boolean - True if Blockchain is Valid, False otherwise
        """
        currBlock = self.getBlock(self.tailBlockHash)
        while currBlock != self.genesisBlock:
            if not self.isValidBlock(currBlock):
                return False
            currBlock = self.getBlock(currBlock.prevHash)
        return True

    def __str__(self):
        string = ""
        currBlock = self.getBlock(self.tailBlockHash)
        while currBlock != self.genesisBlock:
            string += "{} -> ".format(currBlock.currHash)
            currBlock = self.getBlock(currBlock.prevHash)
        return string
