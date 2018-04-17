#!/usr/bin/python3

import hashlib
from ecdsa import VerifyingKey, NIST384p



class Transaction:

    def __init__(self, inputs, outputs):
        """
        Constructor for Transaction

        @param inputs - array of inputs
        @param ouputs - array of outputs
        """
        self.inputs = inputs
        self.outputs = outputs
        self.hash = self.calculateHash()

    def calculateHash(self):
        """
        Calculates Hash for Transaction

        @return Digest - The Digest of the Transaction String
        """
        sha = hashlib.sha256(self.getDataString())
        return str(sha.hexdigest())

    def getDataString(self):
        """
        Calculates Hash for Transaction

        @return String - The String Representation of the Transaction
        """
        value = ""
        for input in self.inputs:
            value += input.hash + str(input.index) + str(input.signature)
        for output in self.outputs:
            value += str(output.pub_key) + str(output.value)
        return value.encode('utf-8')


    def isValid(self, unSpentTransactions):
        """
        Checks if Transaction is Valid

        @param unSpentTransactions - dict{tx_hash -> array of outputs}
        @return If Transaction is valid -> True, False otherwise
        """
        totalValIn = 0.0
        totalValOut = 0.0
        for input in transaction.inputs:
            if input.hash == 'BLOCK-REWARD':
                totalValIn += 5  # Assuming constant reward for now...
            else:
                ref_outs = unSpentTransactions[input.hash]
                ref_out = ref_outs[input.index]
                pub_key = ref_out.pub_key
                signature = inputDict.signature
                vk = VerifyingKey.from_string(pub_key, curve=NIST384p)
                if not vk.verify(signature, rf_tx.getDataString):
                    return False
                totalValIn += ref_out.value
        for outputDict in transaction.outputs:
            totalValOut += output.value
        return totalValIn == totalValOut

    def __str__(self):
        string = "Transaction(\nHash:{}\nInputs:[\n".format(self.hash)
        for input in self.inputs:
            string += input.__str__() + ",\n"
        string += "]\nOutputs:[\n"
        for output in self.outputs:
            string += output.__str__() + ",\n"
        string += "]\n)"
        return string