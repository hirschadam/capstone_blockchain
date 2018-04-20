class Output:
    def __init__(self, pub_key, value):
        """
        Constructor for Output

        @param pub_key - Recipient of Coin
        @param value - Coin of Output
        """
        self.pub_key = pub_key
        self.value = value

    def __str__(self):
        return "Output(\nValue:{}\nPublic Key:{}\n)".format(self.value, str(self.pub_key))
