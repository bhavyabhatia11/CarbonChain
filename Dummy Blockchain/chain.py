import hashlib
from block import Block

class Chain():
    def __init__(self, difficulty):
        self.difficulty = difficulty
        #list that can store our blocks
        self.blocks = []
        #kind of like lobby, 
        #if thers data theyll mine it and add to chain
        self.pool = []
        self.create_origin_block()

    #recives a block and tests it
    def proof_of_work(self,block):
        hash = hashlib.sha256()
        hash.update(str(block).encode('utf-8'))
        #weather or not the block matches the difficulty requirment
        return block.hash.hexdigest() == hash.hexdigest() and int(hash.hexdigest(),16) < 2**(256-self.difficulty)  and block.previous_hash == self.blocks[-1].hash

    def add_to_chain(self,block):
        if self.proof_of_work(block):
            self.blocks.append(block)

    def add_to_pool(self,data):
        self.pool.append(data)

    #create the initial block
    def create_origin_block(self):
        hash = hashlib.sha256()
        hash.update("".encode('utf-8'))
        origin = Block("Origin", hash)
        origin.mine(self.difficulty)
        self.blocks.append(origin)

    #checks if the pool has blocks, mines them and adds it to chain
    def mine(self):
        if len(self.pool) > 0:
            data = self.pool.pop()
            block = Block(data,self.blocks[-1].hash)
            block.mine(self.difficulty)
            self.add_to_chain(block)
            print("\n\n===================================")
            print("Hash : ",block.hash.hexdigest())
            print("Previous Hash : ",block.previous_hash.hexdigest())
            print("Nonce : ",block.nonce)
            print("Data : ",block.data)
            print("\n\n===================================")




