# Online Retail Store (DBMS Project)

Online Retail shop is a comprehensive database-driven application simulating an online retail platform. Designed with a focus on enhancing the customer shopping experience, the system provides tailored functionality for administrators, customers, and sellers to interact efficiently with the inventory and ordering systems.

## Overview

The primary objective of Swift Shop is to streamline and optimize the online shopping experience. It offers robust role-based features for inventory management, order tracking, transaction handling, and customer engagement, backed by a well-structured relational database.

## Assumptions

- Delivery partners are assigned automatically by the system.
- Sellers independently manage the logistics of delivering their products to the platform’s inventory.

## Core Functionalities

### Customer Features

- Browse product catalog by category with real-time pricing and discount visibility
- Add and remove items from cart
- Provide delivery address and complete payment for orders
- View and manage transaction history
- Contact assigned delivery personnel
- Maintain cart items across sessions
- Donate to affiliated NGOs through the ‘Lets Help’ initiative
- Rate and review products and delivery services

### Seller Features

- Add new products under existing categories
- Create new product categories
- Update inventory and manage product listings
- Request delivery partners for customer order fulfillment

### Admin Features

- View and manage data related to customers, sellers, delivery partners, distributors, and NGOs
- Ensure order fulfillment processes are functioning correctly
- Monitor donation funds and allocate a portion of profits to NGO support
- Restock products by contacting distributors
- Provide customers with complete order and transaction history

## Database Schema

### Key Entities and Attributes

#### Admin
- Oversees and monitors the entire platform

#### Products
- Product_ID: Unique identifier
- Category_ID: Links to category
- Name, Price, Quantity, Discount
- Storage_Type, Rating, Description

#### Customers
- Username, Password, Name
- Phone_Number, Address

#### Cart
- Username, Billing_Amount
- Product_IDs and Quantities
- Date of transaction

#### Offers
- Upto_Discount, Category_ID, Expiry_Date

#### Category
- Category_ID, Category_name

#### Orders
- Order_ID, Username, Order_Amount
- Product_IDs, Quantities
- Discounts, Date_Order_Placed

#### Transactions & History
- Billing_ID, Order_ID
- Payment_Mode, Bill_Amount

#### Returns
- Return_ID, Order_ID, Delivery_ID
- Return_Date

#### Track Order
- Tracks delivery status, personnel, vehicle details, estimated time of arrival, delivery ratings, and addresses

#### Seller
- Seller_ID, Password, Name
- Product_IDs, Quantity_sold
- Contact info, Payment_Details, Earnings

#### Inventory
- Maintains availability of products via Product_IDs

## Technical Highlights

- Implementation using SQL with relational schema design and query optimization
- Integration with Python CLI for user interaction
- Automation via triggers for cart and order status
- Data integrity ensured through constraints and normalization
- Role-based access handling for Admin, Customer, and Seller workflows

## Installation & Setup

1. Clone the repository
2. Import the SQL schema and populate the database using provided seed data
3. Run the Python-based CLI to interact with the system
4. Use the SQL interface (e.g., MySQL Workbench or command-line) to query or inspect data

## Contributions

Developed as a semester project under the guidance of Prof. Vikram Goyal. All team members contributed to database design, Python integration, and testing.

## Contact

For questions or collaboration opportunities, contact:

- Kanak Yadav  
- Email: kanak22611@iiitd.ac.in  
- GitHub: [github.com/Kanakyadav88](https://github.com/Kanakyadav88)
