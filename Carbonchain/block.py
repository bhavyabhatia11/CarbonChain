#!/usr/bin/python
# -*- coding: utf-8 -*-


#To use sha256 hash for the blockchain
from hashlib import sha256
import json

#Takes in any number of arguments and produces a sha256 hash as a result
def updatehash(*args):
    hashing_text = ""; h = sha256()

    #loop through each argument and hash
    for arg in args:
        hashing_text += str(arg)

    h.update(hashing_text.encode('utf-8'))
    return h.hexdigest()

#The "node" of the blockchain. Points to the previous block by its unique hash in previous_hash.
class Block():

    #default data for block defined in constructor. Minimum specified should be number and data.
    def __init__(self,number=0, previous_hash="0"*64, data= "", nonce=0):
        self.data = data
        self.number = number
        self.previous_hash = previous_hash
        self.nonce = nonce

    #returns a sha256 hash for the block's data. Function instead of variable in constructor
    #to avoid corruption of the variable.
    def hash(self):
        return updatehash(
            self.number,
            self.previous_hash,
            self.data,
            self.nonce
        )

    #returns a string of the block's data. Useful for diagnostic print statements.
    def __str__(self):
        return str("Block#: %s\nHash: %s\nPrevious: %s\nData: %s\nNonce: %s\n" %(
            self.number,
            self.hash(),
            self.previous_hash,
            self.data,
            self.nonce
            )
        )

