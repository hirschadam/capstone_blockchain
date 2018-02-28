


def __init__(self, private_key=None, public_key=None):
    if private_key is not None and public_key is not None:
        #decode keys
    #generate keys


def sign(self, message):
    """
    Signs a transaction with private key

    @param  message: entire transaction to be signed

    @return         Sha3 hash
    @return_type    string
    """
    #sign message using private key

def verify(self, signature, message, public_key=None):
    """
    Verify a transaction is signed the correct person

    @param  signature: signature to be verified
            message:    transaction that's signed
            public_key: public key of the person who signed the message

    @return         True or False
    @return_type    boolean
    """
    if public_key igs not None:
        #sign and return if true

def getBalance(self, address):
    #query any full node using supplied address

def makeTx(self, to, amount):
    sig = self.sign
