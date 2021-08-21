from app import mysql, session
from blockchain import Block, Blockchain
import json
import string
import random

#custom exceptions for transaction errors
class InvalidTransactionException(Exception): pass
class InsufficientFundsException(Exception): pass

#what a mysql table looks like. Simplifies access to the database 'crypto'
class Table():
    #specify the table name and columns
    #EXAMPLE table:
    #               blockchain
    # number    hash    previous   data    nonce
    # -data-   -data-    -data-   -data-  -data-
    #
    #EXAMPLE initialization: ...Table("blockchain", "number", "hash", "previous", "data", "nonce")
    def __init__(self, table_name, *args):
        self.table = table_name
        self.columns = "(%s)" %",".join(args)
        self.columnsList = args

        #if table does not already exist, create it.
        if isnewtable(table_name):
            create_data = ""
            for column in self.columnsList:
                create_data += "%s varchar(200)," %column

            cur = mysql.connection.cursor() #create the table
            cur.execute("CREATE TABLE %s(%s)" %(self.table, create_data[:len(create_data)-1]))
            cur.close()

    #get all the values from the table
    def getall(self):
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM %s" %self.table)
        data = cur.fetchall(); return data

    #get one value from the table based on a column's data
    #EXAMPLE using blockchain: ...getone("hash","00003f73gh93...")
    def getone(self, search, value):
        data = {}; cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM %s WHERE %s = \"%s\"" %(self.table, search, value))
        if result > 0: data = cur.fetchone()
        cur.close(); return data

    #delete a value from the table based on column's data
    def deleteone(self, search, value):
        cur = mysql.connection.cursor()
        cur.execute("DELETE from %s where %s = \"%s\"" %(self.table, search, value))
        mysql.connection.commit(); cur.close()

    #delete all values from the table.
    def deleteall(self):
        self.drop() #remove table and recreate
        self.__init__(self.table, *self.columnsList)

    #remove table from mysql
    def drop(self):
        cur = mysql.connection.cursor()
        cur.execute("DROP TABLE %s" %self.table)
        cur.close()

    #insert values into the table
    def insert(self, *args):
        data = ""
        for arg in args: #convert data into string mysql format
            data += "\"%s\"," %(arg)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO %s%s VALUES(%s)" %(self.table, self.columns, data[:len(data)-1]))
        mysql.connection.commit()
        cur.close()

#execute mysql code from python
def sql_raw(execution):
    cur = mysql.connection.cursor()
    cur.execute(execution)
    mysql.connection.commit()
    cur.close()

#check if table already exists 
#if not throw exception
def isnewtable(tableName):
    cur = mysql.connection.cursor()

    try: #attempt to get data from table
        result = cur.execute("SELECT * from %s" %tableName)
        cur.close()
    except:
        return True
    else:
        return False

#check if user already exists
def isnewuser(username):
    #access the users table and get all values from column "username"
    users = Table("users", "name", "email", "username", "password")
    data = users.getall()
    usernames = [user.get('username') for user in data]

    return False if username in usernames else True

#send Carbons from one user to another
#Todo: update this function to send carbon instead of money
def send_carbons(sender, recipient, product, units):
    #verify that the amount is an integer or floating value
    try: amount = float(product['carbons']*units)
    except ValueError:
        raise InvalidTransactionException("Invalid Transaction.")

    #verify that the user has enough money to send (exception if it is the BANK)
    if amount > get_balance(sender) and not(is_manu(sender)):
        raise InsufficientFundsException("Insufficient Funds.")

    #verify that the user is not sending money to themselves or amount is less than or 0
    elif sender == recipient or amount <= 0.00:
        raise InvalidTransactionException("Invalid Transaction.")

    #verify that the recipient exists
    elif isnewuser(recipient):
        raise InvalidTransactionException("User Does Not Exist.")
        

    elif not(is_manu(sender)) and not(has_enough_product(sender,product['id'],units)):
        raise InvalidTransactionException("You don't have sufficient units of this product")

    #update the blockchain and sync to mysql
    blockchain = get_blockchain()
    number = len(blockchain.chain) + 1
    #get the rewards associated with the product id
    data = { "sender":sender, 
             "recipient":recipient,
             "carbons":product['carbons']*units,
             "rewards":product['rewards']*units,
             "product_id":product['id'],
             "units":units
            }

    print(str(data))
    
    #data = "%s-->%s-->%s" %(sender, recipient, amount)
    blockchain.mine(Block(number, data=str(data)))
    sync_blockchain(blockchain)

#get the balance of a user
def get_balance(username):
    balance = 0.00
    blockchain = get_blockchain()

    #loop through the blockchain and update balance
    for block in blockchain.chain:
        data = eval(block.data)
        #print(data)
        if username == data['sender']:
            balance -= float(data['carbons'])
        elif username == data['recipient']:
            balance += float(data['carbons'])
    return balance

#get rewards earned by selling carbons of the user
def get_rewards(username):
    rewards = 0.00
    blockchain = get_blockchain()

    #loop through the blockchain and update rewards
    for block in blockchain.chain:
        data = eval(block.data)
        if username == data['sender']:
            rewards += float(data['rewards'])
    return rewards

#get the blockchain from mysql and convert to Blockchain object
def get_blockchain():
    blockchain = Blockchain()
    blockchain_sql = Table("blockchain", "number", "hash", "previous", "data", "nonce")
    #blockchain_sql.deleteall()
    
    for b in blockchain_sql.getall():
        blockchain.add(Block(int(b.get('number')), b.get('previous'), b.get('data'), int(b.get('nonce'))))

    return blockchain

#update blockchain in mysql table
def sync_blockchain(blockchain):
    blockchain_sql = Table("blockchain", "number", "hash", "previous", "data", "nonce")
    blockchain_sql.deleteall()

    for block in blockchain.chain:
        blockchain_sql.insert(str(block.number), block.hash(), block.previous_hash, str(block.data), block.nonce)


#get product data from products table
def get_product(product_id):
    products = Table("products", "id", "name", "details", "maufacturer", "carbons", "rewards")
    product = products.getone("id",product_id)
    return product

#checks and returns true if manufacturer exists
def is_manu(sender):
    products = Table("products", "id", "name", "details", "maufacturer", "carbons", "rewards")
    product = products.getone("maufacturer", sender)
    
    if product: return True
    return False

def has_enough_product(user,product_id,units):
    blockchain = get_blockchain()
    total_units = 0
    #loop through the blockchain and see if user has the product
    for block in blockchain.chain:
        data = eval(block.data)
        if user == data['recipient'] and product_id == data['product_id']:
            total_units += data['units']

    if total_units >= units: return True
    return False

# one timer function to populate the products table
def create_products_table():
    products = Table("products", "id", "name", "details", "maufacturer", "carbons", "rewards")
    for i in range(1,10):
        name = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 10))
        details = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 50))
        maufacturer = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 10))    
        carbons = random.randrange(0, 100, 3)
        rewards = 100-carbons

        products.insert( i, name, details, maufacturer, carbons, rewards)
