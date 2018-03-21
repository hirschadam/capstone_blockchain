#!/usr/bin/python3
#
# Example Input (Dictionary):
#   {
#       "hash": <str>,
#       "index": <integer>,     # Index of the referenced transactions output
#       "signature": <str>
#   }
#
# Example Output (Dictionary):
#   {
#       "value": <float>,
#       "pub_key": <str>
#   }
#
import hashlib


class Transaction:
    '''
    @param inputs - array of input dicts
    @param ouputs - array of output dicts
    '''
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        self.hash = self.calculateHash()

    def calculateHash(self):
        value = ""
        for inputDict in self.inputs:
            value += inputDict['hash'] + str(inputDict['index']) + str(inputDict['signature'])
        for outputDict in self.outputs:
            value += outputDict['pub_key'] + str(outputDict['val'])
        sha = hashlib.sha256(value.encode('utf-8'))
        return str(sha.hexdigest())
