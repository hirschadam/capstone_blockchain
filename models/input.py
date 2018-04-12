class Input:
    def __init__(self, hash, index, signature):
        """
        Constructor for Input

        @param hash - Hash of transaction being referenced for source of Coin
        @param index - Index in Output Array being referenced by TX hash
        @param signature - signature used to validate same person as output referenced
        """
        self.hash = hash
        self.index = index
        self.signature = signature

    def __str__(self):
        return "Input(\nHash:{}\nIndex:{}\nSignature:{}\n)".format(self.hash, self.index, self.signature)
