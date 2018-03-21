#!/usr/bin/python3
#
# Example Input (Dictionary):
#   {
#       "hash": <bytes>,
#       "index": <integer>,     # Index of the referenced transactions output
#       "signature": <bytes>
#   }
#
# Example Output (Dictionary):
#   {
#       "value": <float>,
#       "pub_key": <bytes>
#   }
#


class Transaction:
    '''
    @param inputs - array of input dicts
    @param ouputs - array of output dicts
    '''
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs

                
