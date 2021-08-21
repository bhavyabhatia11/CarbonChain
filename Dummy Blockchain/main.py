from chain import Chain

chain = Chain(20)


for i in range(5):
    data = input("Add something to the block! : ")
    chain.add_to_pool(data)
    chain.mine()



