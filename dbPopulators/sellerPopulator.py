import sqlite3, csv

# DB Connection
connection = sqlite3.connect('db/Project431.db')
cursor = connection.cursor()

# Drop the old table if it exists
cursor.execute('DROP TABLE IF EXISTS Sellers')

# Create the Buyer table (if it doesn't exist already)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Sellers (
    email TEXT PRIMARY KEY,
    business_name TEXT,
    Business_address_id TEXT,
    bank_routing_number TEXT,
    bank_account_number TEXT,
    balance INT,
    FOREIGN KEY (email) REFERENCES Users(email) ON DELETE CASCADE,
    FOREIGN KEY (Business_address_id) REFERENCES Address(address_id)
)
''')

# If data already exists, they will be deleted.
cursor.execute("DELETE FROM Sellers")

# Read data from the CSV file and insert it into the Sellers table
with open('db/NittanyBusinessDataset/Sellers.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip the header row if there is one
    for row in csvreader:
        email,business_name,Business_Address_ID,bank_routing_number,bank_account_number,balance = row
        cursor.execute('''
        INSERT INTO Sellers (email, business_name, Business_Address_ID, bank_routing_number, bank_account_number, balance)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (email, business_name, Business_Address_ID, bank_routing_number, bank_account_number, int(balance)))

# Commit changes and close the connection
connection.commit()
connection.close()

print("Inserted and exited successfully")
