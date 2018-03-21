#!/usr/bin/env python3
import time
import hashlib

class Block:
    def __init__(self, index, prevHash, timestamp, data):
        self.index = index
        self.prevHash = prevHash
        self.timestamp = timestamp
        self.data = data
        self.currHash = self.calculateHash()

    def calculateHash(self):
        value = str(self.index) + str(self.prevHash) + str(self.timestamp) + str(self.data)
        sha = hashlib.sha256(value.encode('utf-8'))
        return str(sha.hexdigest())


    def __eq__(self, other):
        if self.index != other.index:
            return False
        if self.prevHash != other.prevHash:
            return False
        if self.timestamp != other.timestamp:
            return False
        if self.data != other.data:
            return False
        if self.currHash != other.currHash:
            return False
        return True
