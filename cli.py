import mysql.connector
from datetime import datetime, timedelta

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
            5. Exit"""
          )
          
    #SHOULD WE MAKE A DISTRIBUTOR SIGN-UP?

    input_landing_page = int(input("Enter the number: "))
    #ADMIN LOGIN
    if (input_landing_page == 1):
        print("ADMIN")
        print("---------------------------------------------")
        count = 0
        valid_admin = 0
        while(count<3 and valid_admin == 0):
            query_auth_admin = """Select username,password from Admin"""
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            cursor.execute(query_auth_admin)
            for row in cursor.fetchall():
                if (username) == row[0] and (password) == row[1]:
                    # store = row
                    # print(row)
                    valid_admin = 1
                    print("Authenticated\n")
                    break
                
            if valid_admin == 0:
                print("Invalid Username or password\n")
                count+=1
                print(f"{3-count} tries remaining\n")


        while (valid_admin):
            print(f"\nWelcome {username}")
            print("""Please choose a number from the menu to proceed: 
1. View Quarterly Sales of the each Category
2. View Top 5 Customers(based on money spent)
3. Data of items in the Inventory for each storage type
4. Add Category
5. View All Category
6. View all Sellers
7. Log out\n""")
            input_admin = int(input("Enter the number: "))
            
            if (input_admin == 1):
                query_report = """SELECT
    Category.category_name AS Category,
    SUM(Orders.order_amount) AS Total_Sales_Amount,
    SUM(Orders.quantity) AS Total_Quantity_Sold
FROM
    Category
JOIN Products ON Category.category_ID = Products.category_ID
JOIN Orders ON Products.product_ID = Orders.product_ID
JOIN Billing ON Orders.order_ID = Billing.order_ID
WHERE
    Orders.date_order_placed >= DATE_SUB(NOW(), INTERVAL 3 MONTH)
GROUP BY
    Category.category_name  WITH ROLLUP
HAVING
Category IS NOT NULL"""
                
                cursor.execute(query_report)
                print("---------------------------------------------")
                for row in cursor.fetchall():
                    print(f"Category: {row[0]}\nSales from the Category (Rs.): {row[1]}\nQuantity sold (units): {row[2]}")
                    print("---------------------------------------------")
            
            elif (input_admin == 2):
                query_top_5_cust = """SELECT 
                CASE 
                WHEN GROUPING(customer_username) = 1 THEN 'All Customers'
                ELSE customer_username
                END AS Customer,
                SUM(order_amount) AS TotalAmount 
                FROM 
                    Orders
                GROUP BY customer_username with
                    ROLLUP
                HAVING 
                    customer_username IS NOT NULL 
                ORDER BY 
                    TotalAmount DESC 
                LIMIT 
                    5;
                """
                cursor.execute(query_top_5_cust)
                print("---------------------------------------------")
                for row in cursor.fetchall():
                    print(row)
            
            elif (input_admin == 3):    
                query_inv = """SELECT storage_type, SUM(quantity_in_stock) AS amt FROM Products Group by storage_type with ROLLUP having storage_type is not null"""
                cursor.execute(query_inv)
                for row in cursor.fetchall():
                    print(row)

            if (input_admin == 4):
                input_add_category = input("Enter the name of Category that you want to Add: ")
                category_id = int(input("Enter Category ID: "))
                query_category = """INSERT INTO Category(category_ID, category_name) VALUES (%s,%s);"""
                val = (category_id, input_add_category)
                cursor.execute(query_category, val)
                mydb.commit()

            elif (input_admin == 5):
                query = "select * from Category"
                cursor.execute(query)
                for row in cursor.fetchall():
                    print(f"Category ID: {row[0]}, Category Name: {row[1]}")

            elif (input_admin == 6):
                query = "select * from Seller"
                cursor.execute(query)
                for row in cursor.fetchall():
                    print(f"Seller ID: {row[0]}, Seller Name: {row[2]}, Product ID sold: {row[3]}, Quantity Sold: {row[4]}, Phone Number: {row[5]}")

            elif (input_admin == 7):
                break;    
                
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
                    4. Track Order details
                    5. Return details
                    6. Exit to Main Menu""")
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
                    query2 = f"""select Products.product_ID, Products.name, Products.category_ID, Products.price from Category, Products
                    where Products.category_ID = {inp_category} group by Products.product_ID order by Products.product_ID asc
                    """
                    cursor.execute(query2)
                    for row in cursor.fetchall():
                        print(f"{row[0]}: {row[1]}")
                    #accomodating for one quantity inc at a time?
                    inp_id_choice = input("Enter the id of the product you want to add to cart or type exit: ")
                    if inp_id_choice != 'exit':
                        inp_id = int(inp_id_choice)
                        query_3 =  f"""select Products.product_ID, Products.name, Products.price from Products
                        where Products.product_ID = {inp_id}
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
                query_view_cart = f"""select Cart.Quantity, Cart.Billing_Amount, Products.product_ID, Products.name, Cart.product_ID, Cart.Customer_Username from Products, Cart where Products.product_ID = Cart.product_ID"""
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
                query_view_cart = f"""select Cart.quantity, Cart.billing_amount, Products.product_ID, Products.name, Cart.product_ID, Cart.customer_username from Products, Cart where Products.product_ID = Cart.product_ID;"""
                cursor.execute(query_view_cart)
                last_order_id = 0 
                for row in cursor.fetchall():
                    if (row[5] == username):
                        print(f"item name: {row[3]}, quantity: {row[0]}")
                        bill = row[1]
                        query_insert = """insert into Orders (order_ID, Customer_username, order_amount, product_ID, quantity,  date_order_placed) values (%s, %s, %s, %s, %s, CURRENT_DATE())"""

                        #Finding the last order id
                        last_order_id_query = "SELECT MAX(order_id) FROM orders"
                        cursor.execute(last_order_id_query)
                        last_order_id_result = cursor.fetchone()
                        last_order_id = last_order_id_result[0] if last_order_id_result else 0

                        val = (last_order_id+1, username, round(float(bill),2), row[2], row[0])
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

                query_insert = """insert into Billing (billing_ID, payment_mode, bill_amount,  order_ID) values ( %s, %s, %s, %s)"""

                #Finding the last billing id
                last_billing_id_query = "SELECT MAX(billing_id) FROM billing"
                cursor.execute(last_billing_id_query)
                last_billing_id_result = cursor.fetchone()
                last_billing_id = last_billing_id_result[0] if last_billing_id_result else 0

                val = (last_billing_id+1, method_to_pay, round(float(bill_amount),2), last_order_id+1)
                cursor.execute(query_insert,val)
                mydb.commit ()

            # Track Orders Details.
            elif (input_user == 4):   
        
                def track_order(username):
                    # Track Orders Query
                    query_track_orders = """SELECT TrackOrder.delivery_ID, TrackOrder.status, Orders.order_amount, Product.name, TrackOrder.expected_arrival_time
                                            FROM TrackOrder
                                            INNER JOIN Orders ON TrackOrder.order_ID = Orders.order_ID
                                            INNER JOIN Product ON Orders.product_ID = Product.product_ID
                                            WHERE Orders.customer_username = %s"""
                    cursor.execute(query_track_orders, (username,))
                    orders = cursor.fetchall()
                    if orders:
                        print("Your Orders:")
                        for order in orders:
                            print(f"Delivery ID: {order[0]}, Status: {order[1]}, Amount: {order[2]}, Product: {order[3]}, Expected Arrival Time: {order[4]}")

                    else:
                        print("You have no orders yet.")

            # Return Order Details.
            elif(input_user == 5):
                
                # Function to calculate expected return date
                def calculate_expected_return_date(order_date):
                    return order_date + timedelta(days=14)

                # Function to check if a return is within the allowed return period
                def is_within_return_period(order_date_str):
                    try:
                        order_date = datetime.strptime(order_date_str, "%Y-%m-%d")
                        expected_return_date = calculate_expected_return_date(order_date)
                        return datetime.now() <= expected_return_date
                    except ValueError:
                        return False

                while True:
                    order_id = int(input("Enter your Order ID to check return details (Enter 0 to exit): "))
                    if order_id == 0:
                        print("Exiting...")
                        break

                    # Check if the order exists
                    query_check_order = "SELECT * FROM Orders WHERE order_ID = %s"
                    cursor.execute(query_check_order, (order_id,))
                    order_data = cursor.fetchone()

                    if order_data:
                        order_date = order_data[1]
                        if is_within_return_period(order_date):
                            return_date = input("Enter return date (YYYY-MM-DD): ")
                            query_insert_return = "INSERT INTO Return_entity (order_ID, return_date) VALUES (%s, %s)"
                            cursor.execute(query_insert_return, (order_id, return_date))
                            mydb.commit()
                            print("Return order successfully added.")
                        else:
                            print("Return period has expired. You cannot return this order.")
                    else:
                        print("Order not found. Please enter a valid Order ID.")

            elif (input_user == 6):
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
        
        h_no = int(input("Enter house number: "))
        street = input("Enter street name: ")
        city = input("Enter city: ")
        pin = int(input("Enter 6 digit pin code: "))

        query_insert = """insert into Customer (username, password, first_name, last_name, phone_number, house_number, street_name, city, pincode, login_attempts, is_blocked) values (%s,%s,%s,%s,%s,%s,%s,%s,%s, 0,0)"""
        val = (username, password, f_name, l_name, phone,  h_no, street, city, pin)
        cursor.execute(query_insert,val)
        mydb.commit ()
        print ('Successful SignUp')
        print("Redirecting to Home Page")
        #print("\nThe SQL connection is closed.")
    
    elif (input_landing_page == 4):
        while(True):
            query_auth_dist = """Select distributorID,password from Distributor"""
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
                print("Invalid Password \n")
    
    elif(input_landing_page == 5):
        break
    
    else:
        print("Sorry, invalid number")
        print("Please try again\n")
mydb . close ()
if (mydb):
    mydb.close()