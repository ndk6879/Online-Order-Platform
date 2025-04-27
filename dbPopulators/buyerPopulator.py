import sqlite3, csv

# DB Connection
connection = sqlite3.connect('db/Project431.db')
cursor = connection.cursor()

# Drop the old Buyers table if it exists
cursor.execute('DROP TABLE IF EXISTS Buyer')

# Create the Buyer table (if it doesn't exist already)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Buyer (
    email TEXT PRIMARY KEY,
    business_name TEXT,
    buyer_address_id TEXT,
    FOREIGN KEY (email) REFERENCES Users(email) ON DELETE CASCADE,
    FOREIGN KEY (buyer_address_id) REFERENCES Address(address_id)
)
''')

# If data already exists, they will be deleted.
cursor.execute("DELETE FROM Buyer")

# Read data from the CSV file and insert it into the Buyer table
with open('db/NittanyBusinessDataset/Buyers.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip the header row if there is one
    for row in csvreader:
        email, business_name, buyer_address_id = row
        cursor.execute('''
        INSERT INTO Buyer (email, business_name, buyer_address_id)
        VALUES (?, ?, ?)
        ''', (email, business_name, buyer_address_id))

# Commit changes and close the connection
connection.commit()
connection.close()

print("Inserted and exited successfully")
