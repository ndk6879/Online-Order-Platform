
from flask import Flask, render_template, request
import sqlite3, hashlib

app = Flask(__name__)

host = 'http://127.0.0.1:5000/'


# Main/Root Page router with Login
@app.route('/')
def index():
    return render_template('index.html')

# Route to show the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get the form data
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']
        role = request.form['role']

        # Check that the two passwords match
        if password1 != password2:
            return render_template('signup.html', message="Passwords do not match")
        
        # Check that email is not being used
        connection = sqlite3.connect('db/Project431.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE email = ?", (email,))
        result = cursor.fetchone()
        connection.close()
        if not (result is None):
            return render_template('signup.html', message="That email is already in use")

        # Now navigate to the specific signup page
        if role == "Buyer":
            return render_template('buyersignup.html', email= email, password = password1)
        if role == "Seller":
            return render_template('sellersignup.html', email= email, password = password1)
        if role == "HelpDesk":
            return render_template('helpdesksignup.html', email= email, password = password1)

        # For now, just print it
        print(f"Email: {email}")
        print(f"Password: {password1}")
        print(f"Role selected: {role}")

    # If it's a GET request, just render the signup page
    return render_template('signup.html')

# Route to show the sellersignup page
@app.route('/sellersignup', methods=['GET', 'POST'])
def sellersignup():
    if request.method == 'POST':
        # Get Form Data
        email = request.form['email']
        password = request.form['password']
        business_name = request.form['business_name']
        # Bank
        bank_routing_number = request.form['bank_routing_number']
        bank_account_number = request.form['bank_account_number']
        # Address
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        street_num = request.form['street_num']
        street_name = request.form['street_name']

        connection = sqlite3.connect('db/Project431.db')
        cursor = connection.cursor()

        # Add Zipcode
        # If zipcode is not in the table then add it
        cursor.execute("SELECT * FROM Zipcode WHERE zipcode = ?", (zipcode,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute('''
            INSERT INTO Zipcode (zipcode, city, state)
            VALUES (?, ?, ?)
            ''', (zipcode, city, state))
        connection.commit()
        
        # Insert Address
        # Create address id
        Business_Address_ID = hashlib.sha256((zipcode+street_num+street_name).encode()).hexdigest()
        # If address_id is not in the table then add it
        cursor.execute("SELECT * FROM Address WHERE address_id = ?", (Business_Address_ID,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute('''
            INSERT INTO Address (address_id, zipcode, street_num, street_name)
            VALUES (?, ?, ?, ?)
            ''', (Business_Address_ID, zipcode, street_num, street_name))
            connection.commit()

        # Insert User
        cursor.execute('''
        INSERT INTO Users (email, password)
        VALUES (?, ?)
        ''', (email, hashlib.sha256(password.encode()).hexdigest()))
        connection.commit()

        # Insert Seller (Start with a balance of 0)
        cursor.execute('''
        INSERT INTO Sellers (email, business_name, Business_Address_ID, bank_routing_number, bank_account_number, balance)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (email, business_name, Business_Address_ID, bank_routing_number, bank_account_number, 0))
        connection.commit()

        connection.close()

        # For now, just go to login
        return render_template('index.html')

    # If it's a GET request, just render the signup page
    return render_template('sellersignup.html')

# Route to show the buyersignup page
@app.route('/buyersignup', methods=['GET', 'POST'])
def buyersignup():
    if request.method == 'POST':
        # Get Form Data
        email = request.form['email']
        password = request.form['password']
        business_name = request.form['business_name']
        # Address
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        street_num = request.form['street_num']
        street_name = request.form['street_name']
        # Credit Card Information
        credit_card_num = request.form['credit_card_num']
        card_type = request.form['card_type']
        expire_month = request.form['expire_month']
        expire_year = request.form['expire_year']
        security_code = request.form['security_code']

        connection = sqlite3.connect('db/Project431.db')
        cursor = connection.cursor()

        # Add Zipcode
        # If zipcode is not in the table then add it
        cursor.execute("SELECT * FROM Zipcode WHERE zipcode = ?", (zipcode,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute('''
            INSERT INTO Zipcode (zipcode, city, state)
            VALUES (?, ?, ?)
            ''', (zipcode, city, state))
        connection.commit()
        
        # Insert Address
        # Create address id
        address_id = hashlib.sha256((zipcode+street_num+street_name).encode()).hexdigest()
        # If address_id is not in the table then add it
        cursor.execute("SELECT * FROM Address WHERE address_id = ?", (address_id,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute('''
            INSERT INTO Address (address_id, zipcode, street_num, street_name)
            VALUES (?, ?, ?, ?)
            ''', (address_id, zipcode, street_num, street_name))
            connection.commit()

        # Insert User
        cursor.execute('''
        INSERT INTO Users (email, password)
        VALUES (?, ?)
        ''', (email, hashlib.sha256(password.encode()).hexdigest()))
        connection.commit()

        # Insert Buyer
        cursor.execute('''
        INSERT INTO Buyer (email, business_name, buyer_address_id)
        VALUES (?, ?, ?)
        ''', (email, business_name, address_id))
        connection.commit()

        # Insert Credit Card
        cursor.execute('''
        INSERT INTO Credit_Cards (credit_card_num, card_type, expire_month, 
                       expire_year, security_code, owner_email)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (credit_card_num, card_type, expire_month, expire_year, security_code, email))
        connection.commit()
        connection.close()

        # For now, just go to login
        return render_template('index.html')

    # If it's a GET request, just render the signup page
    return render_template('buyersignup.html')

# Route to show the helpdesksignup page
@app.route('/helpdesksignup', methods=['GET', 'POST'])
def helpdesksignup():
    if request.method == 'POST':
        # Get Form Data
        email = request.form['email']
        password = request.form['password']
        Position = request.form['Position']
        admin_code = request.form['admin_code']

        # Because helpdesk accounts can only be done with authorization 
        # we need the correct admin code
        if admin_code != "12345":
            return render_template('helpdesksignup.html', email = email, password = password, message = "Admin Code is not correct")

        connection = sqlite3.connect('db/Project431.db')
        cursor = connection.cursor()

        # Insert User
        cursor.execute('''
        INSERT INTO Users (email, password)
        VALUES (?, ?)
        ''', (email, hashlib.sha256(password.encode()).hexdigest()))
        connection.commit()

        # Insert Helpdesk
        cursor.execute('''
        INSERT INTO Helpdesk (email, Position)
        VALUES (?, ?)
        ''', (email, Position))
        connection.commit()

        connection.close()

        # For now, just go to login
        return render_template('index.html')

    # If it's a GET request, just render the signup page
    return render_template('helpdesksignup.html')


def get_account_type(email):
    connection = sqlite3.connect('db/Project431.db')
    cursor = connection.cursor()

    # Check Buyer table
    cursor.execute('SELECT 1 FROM Buyer WHERE email = ?', (email,))
    if cursor.fetchone():
        connection.close()
        return 'Buyer'

    # Check Seller table
    cursor.execute('SELECT 1 FROM Seller WHERE email = ?', (email,))
    if cursor.fetchone():
        connection.close()
        return 'Seller'

    # Check Helpdesk table
    cursor.execute('SELECT 1 FROM Helpdesk WHERE email = ?', (email,))
    if cursor.fetchone():
        connection.close()
        return 'Helpdesk'

    # If email is not found
    connection.close()
    return None

@app.route('/editaccountinfo', methods=['GET', 'POST'])
def editaccountinfo():
    if request.method == 'POST':
        email = request.form['email']
        # Check what kind of user they are
        account_type = get_account_type(email)
        if account_type == "Buyer":
            return showbuyeraccountinfo(email)
        if account_type == "Seller":
            return showselleraccountinfo(email)
        if account_type == "Helpdesk":
            return showhelpdeskaccountinfo(email)
    if request.method == 'GET':
        return render_template("result.html")

def showbuyeraccountinfo(email):
    print("show buyer account info")
    # Open connection
    connection = sqlite3.connect('db/Project431.db')
    cursor = connection.cursor()

    # Query
    cursor.execute('''
    SELECT 
        b.email,
        b.business_name,
        a.zipcode,
        z.city,
        z.state,
        a.street_num,
        a.street_name
    FROM Buyer b
    JOIN Address a ON b.buyer_address_id = a.address_id
    JOIN Zipcode z ON a.zipcode = z.zipcode
    WHERE b.email = ?
    ''', (email,))

    # Fetch the result
    buyer_info = cursor.fetchone()

    connection.close()

    # unpack the data
    if buyer_info:
        (email, business_name, 
        zipcode, city, state, street_num, street_name) = buyer_info
    else:
        # Handle case where seller not found
        print("Seller not found.")
        return

    #load page with information
    return render_template('editbuyeraccount.html',
                           email = email,
                           business_name = business_name,
                           zipcode = zipcode,
                           city = city,
                           state = state,
                           street_num = street_num,
                           street_name = street_name,
                           )


def showselleraccountinfo(email):
    print("showselleraccountinfo")
    # Open connection
    connection = sqlite3.connect('db/Project431.db')
    cursor = connection.cursor()

    # Query
    cursor.execute('''
    SELECT 
        s.email,
        s.business_name,
        s.bank_routing_number,
        s.bank_account_number,
        a.zipcode,
        z.city,
        z.state,
        a.street_num,
        a.street_name
    FROM Sellers s
    JOIN Address a ON s.Business_Address_ID = a.address_id
    JOIN Zipcode z ON a.zipcode = z.zipcode
    WHERE s.email = ?
    ''', (email,))



    # Fetch the result
    seller_info = cursor.fetchone()

    connection.close()

    # unpack the data
    if seller_info:
        (email, business_name, bank_routing_number, bank_account_number, 
        zipcode, city, state, street_num, street_name) = seller_info
    else:
        # Handle case where seller not found
        print("Seller not found.")
        return
    
    #load page with information
    return render_template('editselleraccount.html',
                           email = email,
                           business_name = business_name,
                           bank_routing_number = bank_routing_number,
                           bank_account_number = bank_account_number,
                           zipcode = zipcode,
                           city = city,
                           state = state,
                           street_num = street_num,
                           street_name = street_name,
                           )

def showhelpdeskaccountinfo(email):
    connection = sqlite3.connect('db/Project431.db')
    cursor = connection.cursor()
    connection.close()
    return

@app.route('/editselleraccount', methods=['Get', 'POST'])
def editselleraccount():
    if request.method == 'POST':
        # Get Form Data
        email = request.form['email']
        business_name = request.form['business_name']
        # Bank
        bank_routing_number = request.form['bank_routing_number']
        bank_account_number = request.form['bank_account_number']
        # Address
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        street_num = request.form['street_num']
        street_name = request.form['street_name']

        # Now update information
        connection = sqlite3.connect('db/Project431.db')
        cursor = connection.cursor()    

        # Add Zipcode
        # If zipcode is not in the table then add it
        cursor.execute("SELECT * FROM Zipcode WHERE zipcode = ?", (zipcode,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute('''
            INSERT INTO Zipcode (zipcode, city, state)
            VALUES (?, ?, ?)
            ''', (zipcode, city, state))
        connection.commit()

        # First, find the seller's Business_Address_ID
        Business_Address_ID = hashlib.sha256((zipcode+street_num+street_name).encode()).hexdigest()
        # If address_id is not in the table then add it
        cursor.execute("SELECT * FROM Address WHERE address_id = ?", (Business_Address_ID,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute('''
            INSERT INTO Address (address_id, zipcode, street_num, street_name)
            VALUES (?, ?, ?, ?)
            ''', (Business_Address_ID, zipcode, street_num, street_name))
            connection.commit()
    
        # Update Sellers table
        cursor.execute('''
        UPDATE Sellers
        SET business_name = ?, bank_routing_number = ?, bank_account_number = ?, Business_Address_ID = ?
        WHERE email = ?
        ''', (business_name, bank_routing_number, bank_account_number, Business_Address_ID, email))
        connection.commit()

        connection.close()

        return showselleraccountinfo(email)
    # If it's a GET request, just render the page
    return render_template('editselleraccount.html')


@app.route('/editbuyeraccount', methods=['Get', 'POST'])
def editbuyeraccount():
    if request.method == 'POST':
        # Get Form Data
        email = request.form['email']
        business_name = request.form['business_name']
        # Address
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        street_num = request.form['street_num']
        street_name = request.form['street_name']

        # Now update information
        connection = sqlite3.connect('db/Project431.db')
        cursor = connection.cursor()    

        # Add Zipcode
        # If zipcode is not in the table then add it
        cursor.execute("SELECT * FROM Zipcode WHERE zipcode = ?", (zipcode,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute('''
            INSERT INTO Zipcode (zipcode, city, state)
            VALUES (?, ?, ?)
            ''', (zipcode, city, state))
        connection.commit()
        
        # Insert Address
        # Create address id
        address_id = hashlib.sha256((zipcode+street_num+street_name).encode()).hexdigest()
        # If address_id is not in the table then add it
        cursor.execute("SELECT * FROM Address WHERE address_id = ?", (address_id,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute('''
            INSERT INTO Address (address_id, zipcode, street_num, street_name)
            VALUES (?, ?, ?, ?)
            ''', (address_id, zipcode, street_num, street_name))
            connection.commit()
    
        # Update Sellers table
        cursor.execute('''
        UPDATE Buyer
        SET business_name = ?, buyer_address_id = ?
        WHERE email = ?
        ''', (business_name, address_id, email))
        connection.commit()

        connection.close()

        return showbuyeraccountinfo(email)
    # If it's a GET request, just render the page
    return render_template('editbuyeraccount.html')

@app.route('/openmanagecreditcards', methods=['POST'])
def open_manage_credit_cards():
    # Called on the edit buyer account when the button for manage credit cards is clicked
    email = request.form['email']
    return render_template('managecreditcards.html', email=email, credit_cards=fetch_credit_cards(email))

@app.route('/deletecreditcard', methods=['POST'])
def delete_credit_card():
    email = request.form['email']
    credit_card_num = request.form['credit_card_num']

    connection = sqlite3.connect('db/Project431.db')
    cursor = connection.cursor()

    # Check how many cards the user has
    cursor.execute('SELECT COUNT(*) FROM Credit_Cards WHERE owner_email = ?', (email,))
    card_count = cursor.fetchone()[0]

    if card_count <= 1:
        # This is the only card, don't delete it
        connection.close()
        message = "Cannot delete the only credit card on your account."
        return render_template('managecreditcards.html', email=email, message=message, credit_cards=fetch_credit_cards(email))
    else:
        # Safe to delete
        cursor.execute('DELETE FROM Credit_Cards WHERE credit_card_num = ? AND owner_email = ?', (credit_card_num, email))
        connection.commit()
        connection.close()
        message = "Card was deleted"
        return render_template('managecreditcards.html', email=email, message=message, credit_cards=fetch_credit_cards(email))

def fetch_credit_cards(email):
    # Returns the list of credit cards on the account with the email
    connection = sqlite3.connect('db/Project431.db')
    cursor = connection.cursor()
    
    # Fetch cards from the database
    cursor.execute('SELECT credit_card_num, card_type, expire_month, expire_year FROM Credit_Cards WHERE owner_email = ?', (email,))
    credit_cards = [
        dict(credit_card_num=row[0], card_type=row[1], expire_month=row[2], expire_year=row[3])
        for row in cursor.fetchall()
    ]

    return credit_cards

@app.route('/managecreditcards', methods=['GET', 'POST'])
def managecreditcards():
    email = request.form['email']
    message = None

    connection = sqlite3.connect('db/Project431.db')
    cursor = connection.cursor()

    if request.method == 'POST':
        
        # Credit Card Information
        credit_card_num = request.form['credit_card_num']
        card_type = request.form['card_type']
        expire_month = request.form['expire_month']
        expire_year = request.form['expire_year']
        security_code = request.form['security_code']

        # Insert Credit Card
        cursor.execute('''
        INSERT INTO Credit_Cards (credit_card_num, card_type, expire_month, 
                       expire_year, security_code, owner_email)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (credit_card_num, card_type, expire_month, expire_year, security_code, email))
        connection.commit()
        message = "Credit Card was added to your account"

    connection.close()
    # Fetch cards from the database
    credit_cards = fetch_credit_cards(email)

    return render_template('managecreditcards.html', email=email, message=message, credit_cards=credit_cards)


# API for handling POST Request for Login functionality
@app.route('/login', methods=['POST'])
def login():
    email, password = request.form['email'], request.form['password']
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # DB conection and querying
    
    #Test ID & PW
    '''
    o5mrsfw0@nittybiz.com	TbIF16hoUqGl
    nnukvpgk@nittybiz.com	MatRuyGWLOmh
    '''
    
    connection = sqlite3.connect('db/Project431.db')
    cursor = connection.cursor()
    cursor.execute("SELECT password FROM Users WHERE email = ?", (email,))
    res = cursor.fetchone()
    connection.close()

    if res and hashed_password == res[0]: message = "Successful Login!"
    else: message = "Username or password is incorrect"

    return render_template('result.html', message=message, email = email)


if __name__ == "__main__":
    app.run()


