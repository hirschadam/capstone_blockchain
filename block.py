#!/usr/bin/env python3
import time
import hashlib
from ecdsa import VerifyingKey, NIST384p

class Block:
    def __init__(self, index, prevHash, timestamp):
        self.index = index
        self.prevHash = prevHash
        self.timestamp = timestamp
        self.transactions = {}
        self.nonce = 0
        self.currHash = self.calculateHash()

    def calculateHash(self):
        value = str(self.index) + str(self.prevHash) + str(self.timestamp) + str(self.nonce)
        for transaction in self.transactions:
            value = transaction.getDataString
        sha = hashlib.sha256(value.encode('utf-8'))
        return str(sha.hexdigest())

    def isValidTransaction(self, transaction, unSpentTransactions):
        totalValIn = 0.0
        totalValOut = 0.0
        for inputDict in transaction.inputs:
            if inputDict['hash'] == 'BLOCK-REWARD':
                totalValIn += 5  # Assuming constant reward for now...
            else:
                ref_tx = unSpentTransactions[inputDict['hash']]
                ref_out = ref_tx.outputs[inputDict['index']]
                pub_key = ref_out['pub_key']
                signature = inputDict['signature']
                vk = VerifyingKey.from_string(pub_key, curve=NIST384p)
                if not vk.verify(signature, rf_tx.getDataString):
                    return False
                totalValIn += ref_out['value']
        for outputDict in transaction.outputs:
            totalValOut += outputDict['value']
        return totalValIn == totalValOut


    def addTransaction(self, transaction, unSpentTransactions):
        if self.isValidTransaction(transaction, unSpentTransactions):
            self.transactions[transaction.hash] = transaction
            return True
        return False

    def removeTransaction(self, transaction):
        if transaction.hash in self.transactions:
            del self.transactions[transaction.hash]
            return True
        return False

    def isValid(self, unSpentTransactions):
        rewardCount = 0
        for transaction in self.transactions:
            if not self.isValidTransaction(transaction, unSpentTransactions):
                return False
            for outputDict in transaction.outputs:
                if outputDict['hash'] == 'BLOCK-REWARD':
                    rewardCount += 1
            if rewardCount > 1:
                return False
        return self.currHash == self.calculateHash()


    def __eq__(self, other):
        if self.index != other.index:
            return False
        if self.prevHash != other.prevHash:
            return False
        if self.timestamp != other.timestamp:
            return False
        if self.transactions != other.transactions:
            return False
        if self.currHash != other.currHash:
            return False
        return True
