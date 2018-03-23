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
from ecdsa import VerifyingKey, NIST384p



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
        sha = hashlib.sha256(self.getDataString())
        return str(sha.hexdigest())

    def getDataString(self):
        value = ""
        for inputDict in self.inputs:
            value += inputDict['hash'] + str(inputDict['index']) + str(inputDict['signature'])
        for outputDict in self.outputs:
            value += outputDict['pub_key'] + str(outputDict['val'])
        return value.encode('utf-8')

    def isValid(self, unSpentTransactions):
        totalValIn = 0.0
        totalValOut = 0.0
        for inputDict in transaction.inputs:
            if inputDict['hash'] == 'BLOCK-REWARD':
                totalValIn += 5  # Assuming constant reward for now...
            else:
                # TODO: change to dict of outputs
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
