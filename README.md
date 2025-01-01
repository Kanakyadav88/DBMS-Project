Swift Shop (Database Management)

Welcome to the repository for the Swift Shop, an Online Retail Store application. This application is designed to streamline the shopping experience, offering a robust platform for customers, sellers, and administrators to manage transactions, track orders, and maintain inventory seamlessly.

Assumptions:
Delivery partners are assigned automatically.
Sellers manage the delivery of their products to the inventory independently.

Main Goal:
The primary focus of our application is to enhance user experience, with a special emphasis on improving the Customer Sector's interactions and functionality.

Database Schema Description
Entities and Attributes

Admin:
Manages and supervises all aspects of the platform.

Products:
Product_ID: Unique identifier for each product.
Category_ID: Links to the product category.
Name: Product name.
Price: Listed price.
Quantity: Stock available.
Discount: Any active discounts.
Storage_Type: Required storage conditions.
Rating: Average user rating.
Description: Brief product description.

Customers:
Username: Unique login identifier.
Password: Secure authentication credential.
Name: Includes first and last names.
Phone_Number: Contact number.
Address: Detailed residential address including house number, street name, city, and pin code.

Cart:
Tied to the customer via Username.
Billing_Amount: Total cost.
{Product_ID}: Products in the cart.
Quantity: Items per product.
Date: Transaction date.

Offers:
Upto_Discount: Maximum available discount.
Category_ID: Applicable product category.
Expiry_Date: Validity of the offer.

Category:
Category_ID: Unique category identifier.
Category_name: Name of the category.

Orders:
Order_ID: Unique order identifier.
Username: Customer's username.
Order_Amount: Total amount.
{Product_ID, Quantity}: Ordered products and their quantities.
Discount: Applied discounts.
Date_Order_Placed: Order date.

Transactions & History:
Billing_ID: Unique billing identifier.
Order_ID: Associated order.
Payment_Mode: Method of payment.
Bill_Amount: Billed amount.

Return:
Return_ID: Unique return transaction identifier.
Order_ID: Linked order.
Delivery_ID: Corresponding delivery.
Return_Date: Processing date for the return.

Track Order:
Details about the delivery process including delivery personnel, vehicle used, current status, associated orders, pickup and delivery addresses, estimated arrival times, and delivery ratings.
Seller
Seller_ID: Unique identifier.
Password: Authentication credential.
{Product_ID}: Products linked to the seller.
Quantity_sold: Total products sold.
Name: Seller's full name.
Phone_Number, Email_ID, Earnings, Payment_Details: Contact and financial information.

Inventory:
product_id: IDs of all products available.

Functionalities
Seller Functionalities:
Introduce new products to existing categories.
Create new categories and add items to them.
Remove products from inventory.
Send delivery requests to partners for customer deliveries.

Customer Functionalities:
Browse the product catalogue with pricing.
Add or remove products from the cart.
Provide delivery address and proceed with payment.
Contact delivery personnel.
Clear the cart or retain items through sessions.
View transaction history.
Donate to affiliated NGOs through 'Lets Help'.
Rate and review products and delivery service.

Admin Functionalities:
Access information on distributors, delivery partners, customers, and affiliated NGOs.
Ensure correct purchase and delivery processes.
Display order history to customers.
Contact distributors for item restocking.
Manage funds from donations and a portion of net profits for NGO support.
