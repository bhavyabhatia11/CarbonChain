# Setup

1. Create a virtual environment
   
   helps to keep everything seperate from the system
   you can install 3rd party in a diffrent container.

   `python3 -m venv env`
    
    `source env/bin/activate`

2. Import HashLib

    hash is a one way cipher, seemingly random not predictable but repeatable

    we will use sha256, a type of hashing function.

    ` import hashlib`

    `h = hashlib.sha256()`

    `h.update('a',encode('utf-8'))`

    `h.hexdigest()`
    

    to learn more refer: https://www.youtube.com/watch?v=f9EbD6iY9zI&t=785s

3. Python Class
   __init__ function will run as soon as the class initialises
   __str__ will return the object as a string

4. Block and Chain object
   we create a chain and use proof of work to verify if the hash is valid or not and then add to chain adds the block to the chain

5. Installing flask and Mysql
   
   pip install flask
   pip install flask-mysqldb
   pip install passlib

6. Creating the Mysql database

   create database <database_name>; \
   use <database_name>; \
   create table <table_name>; \
   select * from <table_name>; 

   Now you have created a database and a table inside that database.
   we can use this to call the database in our app.py which runs our server

7. Running app.py
    app.py is the entry point of the app. To get started with it run app.py

    `python app.py`

   on http://127.0.0.1:5000/ this site will be live. 

N. Limitations
   Mining is a very slow process, using python might not be the right choice to implement a blockchain
   We cannot do memory allocation so our hashing would require formatting