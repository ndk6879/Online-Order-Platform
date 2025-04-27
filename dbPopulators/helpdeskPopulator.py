import sqlite3, csv

# DB Connection
connection = sqlite3.connect('db/Project431.db')
cursor = connection.cursor()

# Drop the old table if it exists
cursor.execute('DROP TABLE IF EXISTS Helpdesk')

# Create the Buyer table (if it doesn't exist already)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Helpdesk (
    email TEXT PRIMARY KEY,
    Position TEXT,
    FOREIGN KEY (email) REFERENCES Users(email) ON DELETE CASCADE
)
''')

# If data already exists, they will be deleted.
cursor.execute("DELETE FROM Helpdesk")

# Read data from the CSV file and insert it into the Helpdesk table
with open('db/NittanyBusinessDataset/Helpdesk.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip the header row if there is one
    for row in csvreader:
        email, Position = row
        cursor.execute('''
        INSERT INTO Helpdesk (email, Position)
        VALUES (?, ?)
        ''', (email, Position))

# Commit changes and close the connection
connection.commit()
connection.close()

print("Inserted and exited successfully")
