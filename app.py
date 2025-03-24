
from flask import Flask, render_template, request
import sqlite3, hashlib

app = Flask(__name__)

host = 'http://127.0.0.1:5000/'


# Main/Root Page router with Login
@app.route('/')
def index():
    return render_template('index.html')



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
    else: message = "Wrong ID or PW"

    return render_template('result.html', message=message)


if __name__ == "__main__":
    app.run()


