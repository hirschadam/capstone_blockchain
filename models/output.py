class Output:
    def __init__(self, value, pub_key):
        """
        Constructor for Output

        @param value - Coin of Output
        @param pub_key - Recipient of Coin
        """
        self.value = value
        self.pub_key = pub_key

    def __str__(self):
        return "Input(\nValue:{}\nPublic Key:{}\n)".format(self.value, self.pub_key)
