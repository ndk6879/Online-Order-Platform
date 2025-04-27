import sqlite3, csv

# DB Connection
connection = sqlite3.connect('db/Project431.db')
cursor = connection.cursor()

cursor.execute('DROP TABLE IF EXISTS Credit_Cards')

# Create the table (if it doesn't exist already)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Credit_Cards (
    credit_card_num TEXT PRIMARY KEY,
    card_type TEXT,
    expire_month TEXT,
    expire_year TEXT,
    security_code TEXT,
    owner_email TEXT NOT NULL,
    FOREIGN KEY (owner_email) REFERENCES Users(email) ON DELETE CASCADE
)
''')

# If data already exists they will be deleted.
cursor.execute("DELETE FROM Credit_Cards")

# Read data from the CSV file and insert it into the table
with open('db/NittanyBusinessDataset/Credit_Cards.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip the header row if there is one
    for row in csvreader:
        credit_card_num, card_type, expire_month, expire_year, security_code, owner_email = row
        cursor.execute('''
        INSERT INTO Credit_Cards (credit_card_num, card_type, expire_month, expire_year, security_code, owner_email)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (credit_card_num, card_type, expire_month, expire_year, security_code, owner_email))


connection.commit()
connection.close()
print("Inserted and exit Successfully")
