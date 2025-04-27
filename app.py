
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
        
        # Insert Address (address id is automatically generated)
        cursor.execute('''
        INSERT INTO Address (zipcode, street_num, street_name)
        VALUES (?, ?, ?)
        ''', (zipcode, street_num, street_name))
        # gets inserted as the last row then we read the generated id
        Business_Address_ID = cursor.lastrowid
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
        
        # Insert Address (address id is automatically generated)
        cursor.execute('''
        INSERT INTO Address (zipcode, street_num, street_name)
        VALUES (?, ?, ?)
        ''', (zipcode, street_num, street_name))
        # gets inserted as the last row then we read the generated id
        address_id = cursor.lastrowid
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

# API for handling GET REQUEST for Login Page 
# @app.route('/login', methods=['GET'])
# def login_page():
#     return render_template('loginPage.html')

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

    return render_template('result.html', message=message)


if __name__ == "__main__":
    app.run()


