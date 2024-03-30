import mysql.connector

# Establish connection
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Karora@88',
    database='online_store_amazon'  # Replace 'your_database_name' with your actual database name
)

# Check if connection is successful
if mydb.is_connected():
    print("Connected to MySQL database")

# Create cursor object
cursor = mydb.cursor()

while(True):
    print("\n")
    print("Online Store Amazon")
    print("Welcome to the Online Retail Store")
    print("---------------------------------------------")
    print("Please choose a number from the menu to proceed: ")
    
    print(
        """ 1. Admin LogIn 
            2. User LogIn
            3. User SignUp
            4. Seller LogIn
            5. NGO funds raised
            6. Exit"""
          )
          
    #SHOULD WE MAKE A DISTRIBUTOR SIGN-UP?

    input_landing_page = int(input("Enter the number: "))
    #ADMIN LOGIN
    if (input_landing_page == 1):
        print("ADMIN")
        print("---------------------------------------------")
        count = 0
        valid_seller = 0
        while(count<3 and valid_seller == 0):
            query_auth_admin = """Select username,password from Seller"""
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            cursor.execute(query_auth_admin)
            for row in cursor.fetchall():
                if (username) == row[2] and (password) == row[1]:
                    # store = row
                    print(row)
                    valid_seller = 1
                    print("Authenticated\n")
                    break
            if valid_seller == 0:
                print("Invalid Username or password\n")
                count+=1
                print(f"{3-count} tries remaining\n")


        while (valid_seller):
            print(f"\nWelcome {username}")
            print("""Please choose a number from the menu to proceed: 


1. View Seller details
2. Log out\n""")
            input_admin = int(input("Enter the number: "))
            
            query_report = """SELECT
Seller.Seller_name AS Seller,
FROM
Seller
JOIN Product ON Category.category_ID = Product.category_ID
JOIN Orders ON Product.product_ID = Orders.product_ID
JOIN Billing ON Orders.order_ID = Billing.order_ID
WHERE
Order.date_order_placed >= DATE_SUB(NOW(), INTERVAL 3 MONTH)
GROUP BY
Category.category_name WITH ROLLUP
HAVING
Category IS NOT NULL"""
                

            query_data = """SELECT
COALESCE(c.category_name, 'All Categories') AS Category,
YEAR(o.date_order_placed) AS Year,
MONTH(o.date_order_placed) AS Month,
SUM(o.order_amount) AS Sales,
COUNT(DISTINCT o.username) AS Customers,
COUNT(DISTINCT o.product_ID) AS Products
FROM
Order o
JOIN Product p ON o.product_ID = p.product_ID
JOIN Category c ON p.categoryID = c.categoryID
GROUP BY Category, Year, Month with ROLLUP
HAVING
Month is NOT NULL
ORDER BY Category, Year DESC, Month DESC;"""
           

            
            if (input_admin == 1):
                query = "select * from Seller"
                cursor.execute(query)
                for row in cursor.fetchall():
                    print(f"Category ID: {row[0]}, Category Name: {row[1]}")

            elif (input_admin == 2):
                break
                
            else:
                print("Invalid Input!")


    #USER LOGIN
    elif (input_landing_page == 2):
        count = 0
        valid_user = 0
        while(count<3 and valid_user == 0):
            query_auth_user = """Select username,password from Customer"""
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            cursor.execute(query_auth_user)
            for row in cursor.fetchall():
                if (username) == row[0] and (password) == row[1]:
                    # store = row
                    # print(row)
                    valid_user = 1
                    print("Authenticated\n")
                    break
            if valid_user == 0:
                print("Invalid Username or password\n")
                count+=1
                print(f"{3-count} tries remaining\n")

        while(valid_user):
            print(f"Welcome {username}")
            print("---------------------------------------------")
            print("Please choose a number from the menu to proceed: ")
            print("""1. View Categories
                    2. View Cart
                    3. Proceed To Checkout
                    4. Exit to Main Menu""")
            input_user = int(input("Enter the number from the menu: "))
            if (input_user == 1):
                query = "select category_name from Category"
                cursor.execute(query)
                i = 1
                print("\nSelect the Category from below or type exit: ")
                for row in cursor.fetchall():
                    print(f"{i}: {row[0]}")
                    i+=1
                inp_customer = input()
                if inp_customer != 'exit':
                    inp_category = int(inp_customer)
                    query2 = f"""select Product.product_ID, Product.name, Product.category_ID, Product.price from Category, Product
                    where Product.category_ID = {inp_category} group by Product.product_ID order by Product.product_ID asc
                    """
                    cursor.execute(query2)
                    for row in cursor.fetchall():
                        print(f"{row[0]}: {row[1]}")
                    #accomodating for one quantity inc at a time?
                    inp_id_choice = input("Enter the id of the product you want to add to cart or type exit: ")
                    if inp_id_choice != 'exit':
                        inp_id = int(inp_id_choice)
                        query_3 =  f"""select Product.product_ID, Product.name, Product.price from Product
                        where Product.product_ID = {inp_id}
                        """
                        cursor.execute(query_3)
                        
                        query_cart = """insert into Cart (Billing_Amount, product_ID, Quantity, Customer_username) values (%s, %s, %s, %s)"""
                        for row in cursor.fetchall():
                            id = row[0]
                            quantity = 1
                            cost = row[2]
                        val = (cost, id, quantity, username)
                        cursor.execute(query_cart,val)
                        mydb.commit ()

            elif (input_user == 2):
                query_view_cart = f"""select Cart.Quantity, Cart.Billing_Amount, Product.product_ID, Product.name, Cart.product_ID, Cart.Customer_Username from Product, Cart where Product.product_ID = Cart.product_ID"""
                cursor.execute(query_view_cart)
                bill = 0
                for row in cursor.fetchall():
                    if (row[5] == username):
                        print(f"item name: {row[3]}, quantity: {row[0]}")
                        bill = row[1]
                print(f"billing amount: {bill}")

            elif (input_user == 3):
                #checkout or placing an order
                print("Items in your cart: ")
                query_view_cart = f"""select Cart.quantity, Cart.billing_amount, Product.product_ID, Product.name, Cart.product_ID, Cart.username from Product, Cart where Product.product_ID = Cart.product_ID"""
                cursor.execute(query_view_cart)

                for row in cursor.fetchall():
                    if (row[5] == username):
                        print(f"item name: {row[3]}, quantity: {row[0]}")
                        bill = row[1]
                        query_insert = """insert into Orders (order_ID, Customer_username, order_amount, product_ID, quantity,  date_order_placed) values (%s, %s, %s, %s, %s, %s)"""
                        val = (12, username, 'order_received', round(float(bill),2), row[2], row[0], 0)
                        cursor.execute(query_insert,val)
                        mydb.commit ()

                bill_amount = bill
                # bill_amount = 0
                # for row in cursor.fetchall():
                #     if (row[5] == username):
                #         print(f"item name: {row[3]}, quantity: {row[0]}")
                #         bill_amount = row[1]
                # print(f"billing amount: {bill_amount}")

                method_to_pay = input("Method to pay (COD/UPI/card/wallet) : ")

                query_insert = """insert into Billing (billingID, payment_mode, bill_amount,  order_ID) values ( %s, %s, %s, %s)"""
                val = (111, method_to_pay, round(float(bill_amount),2), 12)
                cursor.execute(query_insert,val)
                mydb.commit ()

            elif (input_user == 4):
                break

            else:
                print("Invalid Input!")

    #USER SIGN UP
    elif (input_landing_page == 3):
        print("User SignUp")
        username = input("Set your username: ")
        password = input("Set your password: ")
        f_name = input("Enter First Name: ")
        l_name = input("Enter Last Name: ")
        phone = input("Enter phone number: ")
        mail = input("Enter email id: ")
        subs_type = 'regular'
        #hardcoded 
        coupon_id = 99999
        h_no = int(input("Enter house number: "))
        street = input("Enter street name: ")
        city = input("Enter city: ")
        pin = int(input("Enter 6 digit pin code: "))

        query_insert = """insert into Customer (username, password, first_name, last_name, phone_number, email_address, subscription_type, coupon_ID, house_number, street_name, city, pincode) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s)"""
        val = (username, password, f_name, l_name, phone, mail, subs_type, coupon_id, h_no, street, city, pin)
        cursor.execute(query_insert,val)
        mydb.commit ()
        print ('Successful SignUp')
        print("Redirecting to Home Page")
        #print("\nThe SQL connection is closed.")
    
    elif (input_landing_page == 4):
        while(True):
            query_auth_dist = """Select distributor_ID,password from Distributor"""
            id_dist = int(input("Enter your Distributor ID: "))
            cursor.execute(query_auth_dist)
            valid_user = 0
            for row in cursor.fetchall():
                if (id_dist) == row[0]:
                    store = row
                    print(row)
                    valid_user = 1
                    break
            if valid_user:
                break
            else: 
                print("Invalid ID\n")

        while(True):
            password = input("Enter your password: ")
            if password in store:
                print("Authenticated")
                break
            else:
                print("Invalid Username or password\n")
                count+=1
                print(f"{3-count} tries remaining\n")


        while (valid_admin):
            print(f"\nWelcome {username}")
            print("""Please choose a number from the menu to proceed: 


1. Add Category
2. View All Category
3. Log out\n""")
            input_admin = int(input("Enter the number: "))
            
            query_report = """SELECT
Category.category_name AS Category,
FROM
Category
JOIN Product ON Category.category_ID = Product.category_ID
JOIN Orders ON Product.product_ID = Orders.product_ID
JOIN Billing ON Orders.order_ID = Billing.order_ID
WHERE
Order.date_order_placed >= DATE_SUB(NOW(), INTERVAL 3 MONTH)
GROUP BY
Category.category_name WITH ROLLUP
HAVING
Category IS NOT NULL"""
                

            query_data = """SELECT
COALESCE(c.category_name, 'All Categories') AS Category,
YEAR(o.date_order_placed) AS Year,
MONTH(o.date_order_placed) AS Month,
SUM(o.order_amount) AS Sales,
COUNT(DISTINCT o.username) AS Customers,
COUNT(DISTINCT o.product_ID) AS Products
FROM
Order o
JOIN Product p ON o.product_ID = p.product_ID
JOIN Category c ON p.categoryID = c.categoryID
GROUP BY Category, Year, Month with ROLLUP
HAVING
Month is NOT NULL
ORDER BY Category, Year DESC, Month DESC;"""
           

            if (input_admin == 1):
                input_add_category = input("Enter the name of Category that you want to Add: ")
                #PLEASE CHECK IF WE CAN ALSO INSERT ONE PRODUCT WHILE WE MAKE A CATEGORY, I HAVE LEFT THAT OUT RN
                #input_prod = input(f"Enter the name of one product to add in {input_add_category}")
                category_id = int(input("Enter Category ID: "))
                query_category = """INSERT INTO Category(category_ID, category_name) VALUES (%s,%s);"""
                val = (category_id, input_add_category)
                cursor.execute(query_category, val)
                mydb.commit()

            elif (input_admin == 2):
                query = "select * from Category"
                cursor.execute(query)
                for row in cursor.fetchall():
                    print(f"Category ID: {row[0]}, Category Name: {row[1]}")

            elif (input_admin == 3):
                break
                
            else:
                print("Invalid Input!")
    

    elif(input_landing_page == 6):
        break
    
    else:
        print("Sorry, invalid number")
        print("Please try again\n")
mydb . close ()
if (mydb):
    mydb.close()