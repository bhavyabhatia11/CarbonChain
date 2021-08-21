import hashlib

# Some abstract structure that we wll use to store data
class Block():
    #runs whenever an object of class Block is created
    def __init__(self,data,previous_hash):
        self.hash = hashlib.sha256()
        self.previous_hash = previous_hash #links the blocks with previous
        self.nonce = 0
        self.data = data

    #mine a block for us, amount of work to do get the hash of a block
    def mine(self,difficulty):
        self.hash.update(str(self).encode('utf-8'))

        while int(self.hash.hexdigest(),16) > 2**(256-difficulty):
            self.nonce +=1
            self.hash = hashlib.sha256()
            self.hash.update(str(self).encode('utf-8'))

    #runs whenever you pass this object into a parameter
    #in which it is being treated as a string
    def __str__(self):
        return "Previous hash : {}  Data: {}  Nonce Number : {}".format(self.previous_hash.hexdigest() ,self.data,self.nonce)

         