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

# Embedded Query 1
def order_items(username, product_id, quantity):
    try:
        # Check the quantity of the items of the product id
        cmd = "SELECT quantity_in_stock FROM products WHERE product_id = %s"
        cursor.execute(cmd, (product_id,))
        result = cursor.fetchone()
        available_quantity = result[0] if result else 0

        if available_quantity < quantity:
            print("Error: Insufficient quantity available for product with ID:", product_id)
        else:
            # Proceed with the order
            # Fetch the last order id
            last_order_id_query = "SELECT MAX(order_id) FROM orders"
            cursor.execute(last_order_id_query)
            last_order_id_result = cursor.fetchone()
            last_order_id = last_order_id_result[0] if last_order_id_result else 0

            # Fetch the price corresponding to the given product ID
            price_query = "SELECT price FROM products WHERE product_id = %s"
            cursor.execute(price_query, (product_id,))
            price_result = cursor.fetchone()
            price = price_result[0] if price_result else 0

            # Calculate order amount
            order_amount = price * quantity

            # Insert into Orders table
            insert_query = "INSERT INTO orders (order_id, customer_username, order_amount, product_id, quantity, date_order_placed) VALUES (%s, %s, %s, %s, %s, CURDATE())"
            cursor.execute(insert_query, (last_order_id + 1, username, order_amount, product_id, quantity))

            mydb.commit()  # Commit the transaction

            print("Order placed successfully.")

    except mysql.connector.Error as error:
        print("Failed to execute query:", error)

# Embedded Query 2
def product_quantity_analysis():
    try:
        cursor.execute("SELECT name, quantity_in_stock FROM products WHERE quantity_in_stock < 100")
        low_inventory_items = cursor.fetchall()
        print("Items with low inventory:")
        for item in low_inventory_items:
            print(item)
    except mysql.connector.Error as error:
        print("Failed to execute query:", error)

# Embedded Query 3
def search_by_key_word(key_word):
    try:
        cmd = "SELECT name, description, price FROM products WHERE name LIKE %s"
        cursor.execute(cmd, ('%' + key_word + '%',))
        search_results = cursor.fetchall()
        print("Search results:")
        for result in search_results:
            print(result)
    except mysql.connector.Error as error:
        print("Failed to execute query:", error)

# Example usage
order_items("user2", 3, 2)
product_quantity_analysis()
search_by_key_word("ild")

# Close cursor and connection
cursor.close()
mydb.close()
