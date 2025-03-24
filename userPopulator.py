import sqlite3, csv, hashlib

# DB Connection
connection = sqlite3.connect('db/Project431.db')
cursor = connection.cursor()

# Users Table Initialization
# If data already exists in the table, they will be deleted.
cursor.execute("DELETE FROM Users")

# Open CSV file
with open('db/Users.csv', newline='', encoding='utf-8') as csvf:
    reader = csv.DictReader(csvf)  #read email and password on the first line of csv file
    for r in reader:

        #get email and password and then hash the password by using the hashlib library
        email, password = r['email'], r['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Insert email and hashed password
        cursor.execute("INSERT INTO Users (email, password) VALUES (?, ?)", (email, hashed_password))

# 6. store and exit
connection.commit()
connection.close()
print("Inserted and exit Successfully")
