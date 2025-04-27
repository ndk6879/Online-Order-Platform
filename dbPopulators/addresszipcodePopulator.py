import sqlite3, csv

# DB Connection
connection = sqlite3.connect('db/Project431.db')
cursor = connection.cursor()

# Address and Zipcode Table Initialization
cursor.execute('DROP TABLE IF EXISTS Address')
cursor.execute('DROP TABLE IF EXISTS Zipcode')

# Create the Zipcode table (if it doesn't exist already)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Zipcode (
    zipcode TEXT PRIMARY KEY,
    city TEXT,
    state TEXT
)
''')

# Create the Address table (if it doesn't exist already)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Address (
    address_id TEXT PRIMARY KEY,
    zipcode TEXT,
    street_num TEXT,
    street_name TEXT,
    FOREIGN KEY (zipcode) REFERENCES Zipcode(zipcode)
)
''')

# If data already exists they will be deleted.
cursor.execute("DELETE FROM Address")
cursor.execute("DELETE FROM Zipcode")

# Read data from the CSV file and insert it into the Address table
with open('db/NittanyBusinessDataset/Address.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip the header row
    for row in csvreader:
        address_id, zipcode, street_num, street_name = row
        cursor.execute('''
        INSERT INTO Address (address_id, zipcode, street_num, street_name)
        VALUES (?, ?, ?, ?)
        ''', (address_id, zipcode, street_num, street_name))

# Read data from the CSV file and insert it into the Zipcode table
with open('db/NittanyBusinessDataset/Zipcode_Info.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip the header row if there is one
    for row in csvreader:
        zipcode, city, state = row
        cursor.execute('''
        INSERT INTO Zipcode (zipcode, city, state)
        VALUES (?, ?, ?)
        ''', (zipcode, city, state))

connection.commit()
connection.close()
print("Inserted and exit Successfully")
