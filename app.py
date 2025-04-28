from flask import Flask, render_template, request, redirect
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

#1. User Login
# API for handling POST Request for Login functionality
#4.26: Login works with new ID/PW from User Registration form

@app.route('/login', methods=['POST'])
def login():
    email, password = request.form['email'], request.form['password']
    NewHashedPassword = hashlib.sha256(password.encode()).hexdigest()

    
    #Test ID & PW
    '''
    o5mrsfw0@nittybiz.com	TbIF16hoUqGl
    nnukvpgk@nittybiz.com	MatRuyGWLOmh
    '''

    # DB conection and querying    
    connection = sqlite3.connect('db/Project431.db')
    cursor = connection.cursor()
    cursor.execute("SELECT password FROM Users WHERE email = ?", (email,))
    res = cursor.fetchone()
    connection.close()
    # print('res:',res)

    if res and NewHashedPassword == res[0]: message = "Successful Login!"
    else: message = "Wrong ID or PW"

    return render_template('result.html', message=message)
    


#(OK) 2. Category Hierarchy
# API for handling and showing categories, subcategories, and products
@app.route('/categories/<parentName>')
def Category(parentName):

    #connect to our Project431 database with cursor
    connection = sqlite3.connect('db/Project431.db')
    cursor = connection.cursor()

    # DB call for selecting category
    cursor.execute(""" SELECT category_name FROM Categories WHERE parent_category = ? """, (parentName,))
    subcategories = [row[0] for row in cursor.fetchall()]
    # print('subcategories:',subcategories)

    # DB call for products
    cursor.execute("""SELECT Product_Title FROM Product_Listings WHERE Category = ? """, (parentName,))
    products = []
    for r in cursor.fetchall():
        products.append(r[0])
    # print('products:',products)

    connection.close()

    # key & values are used in category_view.html
    data = {'parent': parentName, 'subcategories': subcategories, 'products': products}
    return render_template('CategoryView.html', **data)

#(OK) API for redirecting to Root 
@app.route('/categories')
def MainCategoryWithRoot():
    return redirect('/categories/Root')













#3. Product Listing Management
# (OK) API to display page to show the product listings
@app.route('/products')
def ProductList():

    #connect to our Project431 database with cursor and take products
    connection = sqlite3.connect('db/Project431.db')
    cursor = connection.cursor()
    cursor.execute("SELECT Listing_ID,Product_Title,Category,Quantity,Product_Price,Status FROM Product_Listings")
    Allproduct = cursor.fetchall()
    connection.close()

    return render_template('productList.html', Allproduct=Allproduct)


#3. API to add product 
@app.route('/products/add', methods=['GET', 'POST'])
def AddProduct():
    
    #connect to our Project431 database with cursor
    connection = sqlite3.connect('db/Project431.db')
    cursor = connection.cursor()

    #Because max of Listing_ID was around 2700, maxID compares with 2700 + if the request is POST, we handle form data
    if request.method == 'POST':
        cursor.execute("SELECT MAX(Listing_ID) FROM Product_Listings")
        # Take the maximum ID
        maxID = cursor.fetchone()[0]
        print('maxID:',maxID)

        # For new Listing_ID
        if not maxID or maxID < 2700:
            new_id = 2700
        else:
            new_id = maxID + 1

        # Form Data
        quantity = int(request.form['quantity'])
        title = request.form['title']
        category = request.form['category']
        status = int(request.form['status']) #1 => active, 2 => inactive
        price = float(request.form['price'])

        # Insert Data
        cursor.execute("""
            INSERT INTO Product_Listings (Listing_ID, Seller_email, Category, Product_Title, Quantity, Product_Price, Status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (new_id, 'test_seller@nittybiz.com', category, title, quantity, price, status))

        connection.commit()
        connection.close()

        return redirect('/products')

    connection.close()
    return render_template('AddProduct.html')



# OK 3. API to edit product 
@app.route('/products/edit/<int:ListingID>', methods=['GET', 'POST'])
def EditProduct(ListingID):
    connection = sqlite3.connect('db/Project431.db')
    cursor = connection.cursor()

    if request.method == 'POST':
        #Update Form Data
        title = request.form['title']
        category = request.form['category']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        status = int(request.form['status'])

        cursor.execute(""" UPDATE Product_Listings SET Product_Title = ?, Category = ?, Quantity = ?, Product_Price = ?, Status = ? WHERE Listing_ID = ? """, 
        (title, category, quantity, price, status, ListingID))
        connection.commit()
        connection.close()
        return redirect('/products')

    # Call for Product from DB
    cursor.execute(""" SELECT Product_Title, Category, Quantity, Product_Price, Status FROM Product_Listings WHERE Listing_ID = ? """, (ListingID,))
    product = cursor.fetchone()
    connection.close()

    data = {'product': product, 'ListingID': ListingID}
    return render_template('EditProduct.html', **data)



#3. API to delete product 
@app.route('/products/delete/<int:ListingID>', methods=['GET'])
def DeleteProduct(ListingID):
    connection = sqlite3.connect('db/Project431.db')
    cursor = connection.cursor()

    # Delete the product accordingly 
    cursor.execute("DELETE FROM Product_Listings WHERE Listing_ID = ?", (ListingID,))
    connection.commit()
    connection.close()

    return redirect('/products')







#4. Order Management
@app.route('/products/buy/<int:ListingID>', methods=['GET', 'POST'])
def BuyProduct(ListingID):

    #connect to our Project431 database with cursor
    connection = sqlite3.connect('db/Project431.db')
    cursor = connection.cursor()

    # if "Purchase" button is clicked
    if request.method == 'POST':

        #get the qunatity user entered in the form
        OrderQuantity = int(request.form['quantity'])

        # Bring product info from database
        cursor.execute(""" SELECT Quantity, Product_Price, Seller_Email FROM Product_Listings WHERE Listing_ID = ? """, (ListingID,))
        product = cursor.fetchone()

        # if there's no product, then we close our database and return 494 with error message
        if not product:
            connection.close()
            return "There is no Product available", 404
            
        #get current quantity, raw price, and seller email from the product we're trying to buy
        CurrentQuantity, RawPrice, SellerEmail = product
        price = float(str(RawPrice).replace('$', '').replace(',', '').strip())
        print("Seller Email:", SellerEmail)
        
        # if the order quantity is more than the quantity of product currently having, we just return the message
        if OrderQuantity > CurrentQuantity:
            connection.close()
            return "Not enough stock", 400

        # Handle Quantity for proper calculation
        CurrQuantity = CurrentQuantity - OrderQuantity
        new_status = 0
        if CurrQuantity == 0:
            new_status = 2
        else:
            new_status = 1
            

        #Otherwise, everything is correct so we update our row of DB 
        cursor.execute(""" UPDATE Product_Listings SET Quantity = ?, Status = ? WHERE Listing_ID = ? """, (CurrQuantity, new_status, ListingID))

        # Update seller's balance
        total = int(OrderQuantity * price)
        cursor.execute(""" UPDATE Sellers SET balance = balance + ? WHERE email = ? """, (total, SellerEmail))


        #close our DB
        connection.commit()
        connection.close()

        return redirect('/products')

    #close DB
    connection.close()
    return render_template('BuyProduct.html', ListingID=ListingID)






#5. Product & Seller Review
#5-1. Leave review in http://127.0.0.1:5000/reviews/add/2589. then review will leave in DB Review table.
# display form page for review
@app.route('/reviews/add/<int:ListingID>', methods=['GET'])
def ReviewForm(ListingID):
    return render_template('AddReview.html', ListingID=ListingID)


# 5-2. Once we make a review of a product, review will be left Review table and rating will be left in the Seller.  
# If review already exists in the Seller's table, the rating will be calculated accumulatively with the previous ratings.
# Each Review will be added in a Review table.
@app.route('/reviews/add/<int:ListingID>', methods=['POST'])
def AddReview(ListingID):
    #get rating and description from the form that users entered.
    rating, desc = int(request.form['rating']), request.form['description']

    #connect to our Project431 database with cursor
    conn = sqlite3.connect('db/Project431.db')
    cursor = conn.cursor()

    # find the email of product seller from product listing table
    cursor.execute("SELECT Seller_Email FROM Product_Listings WHERE Listing_ID = ?", (ListingID,))
    seller = cursor.fetchone()

    if seller:
        seller_email = seller[0]

        # Save Review in the review table with rating and description
        cursor.execute("""INSERT INTO Reviews (Order_ID, Rate, Review_Desc) VALUES (?, ?, ?)
        """, (ListingID, rating, desc))

        # Calculate the new rate of seller with previous ratings
        cursor.execute("""SELECT AVG(Rate) FROM Reviews JOIN Product_Listings ON Reviews.Order_ID = Product_Listings.Listing_ID WHERE Seller_Email = ? """, (seller_email,))
        AllRating = cursor.fetchone()[0]

        # if this rating is the first one, we just set this rating as the current rating
        if AllRating is not None:
            # Update Seller table
            cursor.execute(""" UPDATE Sellers SET rating = ? WHERE email = ? """, (AllRating, seller_email))

    #close our DB
    conn.commit()
    conn.close()

    return redirect('/products')





#6. Product Search
#Show search page
@app.route('/search', methods=['GET'])
def SearchForm():
    return render_template('search.html')


# Handle search result
@app.route('/search', methods=['POST'])
def SearchResults():

    #connect to our Project431 database with cursor
    conn = sqlite3.connect('db/Project431.db')
    cursor = conn.cursor()

    #get keyword from the user's input form
    keyword = request.form['keyword']

    #find what input keywords are contained
    query = """SELECT Listing_ID, Product_Title, Product_Description, Product_Price FROM Product_Listings WHERE Product_Title LIKE ? OR Product_Description LIKE ? """
    LikeKeywords = f"%{keyword}%"
    cursor.execute(query, (LikeKeywords, LikeKeywords))
    resultAll = cursor.fetchall()

    #close our DB
    conn.close()

    data = {'resultAll': resultAll, 'keyword': keyword}
    return render_template('SearchResults.html', **data)












#7. User Registration
# API to show register form page
@app.route('/register', methods=['GET'])
def RegisterForm():
    return render_template('Register.html')

# API to register user and save email/password in the User table
@app.route('/register', methods=['POST'])
def register():
    # email and password from the form input
    email, password = request.form['email'],request.form['password']

    # hash password will be saved in the User table for security
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    #connect to our Project431 database with cursor
    conn = sqlite3.connect('db/Project431.db')
    cursor = conn.cursor()

    try:
        # save email and password in Users table
        cursor.execute(""" INSERT INTO Users (email, password) VALUES (?, ?) """, (email, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        # If email already exists, then just close
        conn.close()
        return "Email registered already"

    #close our DB
    conn.close()
    return redirect('/')









#8. User Profile Update
# API to show and update user email and password
@app.route('/profile', methods=['GET'])
def ProfileForm():
    return render_template('profile.html')


#8. User Profile Update
# API to update user's profile(update user email and password in DB table)
@app.route('/profile', methods=['POST'])
def UpdateProfile():
    email, newPassword = request.form['email'], request.form['new_password']
    hashedPassword = hashlib.sha256(newPassword.encode()).hexdigest()

    #connect to our Project431 database with cursor and store new email and password for update
    conn = sqlite3.connect('db/Project431.db')
    cursor = conn.cursor()
    cursor.execute(""" UPDATE Users SET password = ? WHERE email = ? """, (hashedPassword, email))
    conn.commit()
    conn.close()

    return redirect('/')



if __name__ == "__main__":
    app.run()


