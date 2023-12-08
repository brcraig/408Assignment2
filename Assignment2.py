import sys
import mysql.connector

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host = '34.102.125.152',
            port = '3306',
            user = 'root',
            password = 'cloudpython1!',
            database = 'FSE EngStore'
        )
        return conn
    except mysql.connector.Error as e:
        print(f"error connecting to mysql: {e}")
        return None

def execute_query(conn, query, query_description):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        print(query_description)
        for row in result:
            print(row)
    except mysql.connector.Error as e:
        print(f"Error executing query: {e}")

def list_out_of_stock_products(conn):
    query = "SELECT * FROM Products WHERE UnitsInStock = 0;"
    query_description = "List all products that are out of stock:"
    execute_query(conn, query, query_description)

def total_orders_per_customer(conn):
    query = """
    SELECT c.CustomerID, c.CustomerName, COUNT(o.OrderID) as TotalOrders
    FROM Customers c
    LEFT JOIN Orders o ON c.CustomerID = o.CustomerID
    GROUP BY c.CustomerID;
    """
    query_description = "Find the total number of orders placed by each customer:"
    execute_query(conn, query, query_description)

def most_expensive_products_in_each_order(conn):
    query = """
    SELECT od.OrderID, p.ProductName, MAX(p.UnitPrice) as MaxUnitPrice
    FROM OrderDetails od
    JOIN Products p ON od.ProductID = p.ProductID
    GROUP BY od.OrderID, p.ProductName;
    """
    query_description = "Display the details of the most expensive product ordered in each order:"
    execute_query(conn, query, query_description)

def products_never_ordered(conn):
    query = """
    SELECT p.ProductName
    FROM Products p
    LEFT JOIN OrderDetails od ON p.ProductID = od.ProductID
    WHERE od.ProductID IS NULL;
    """
    query_description = "Retrieve a list of products that have never been ordered:"
    execute_query(conn, query, query_description)

def total_revenue_by_supplier(conn):
    query = """
    SELECT s.SupplierID, s.SupplierName, SUM(p.UnitPrice * od.Quantity) as TotalRevenue
    FROM Suppliers s
    JOIN Products p ON s.SupplierID = p.SupplierID
    JOIN OrderDetails od ON p.ProductID = od.ProductID
    GROUP BY s.SupplierID;
    """
    query_description = "Show the total revenue (price * quantity) generated by each supplier:"
    execute_query(conn, query, query_description)

def add_new_order(conn):
    try:
        cursor = conn.cursor()
        customer_id = input("What is the customer ID: ")
        while True:
            if(customer_id.isdigit()):
                break
            else:
                customer_id = input("Invalid customer ID, try again:")
        order_date_pattern = "^\(\d{4})\) (\d{2}) - (\d{2})"
        order_date = input("What is the order date(Year-month-day): ")
        ship_date_pattern = "^\(\d{4})\) (\d{2}) - (\d{2})"
        ship_date = input("What is the ship date(Year-month-day): ")
        ship_address = input("What is the shipping address: ")
        ship_city = input("What is the shipping city: ")
        ship_postal_code = input("What is the shipping postal code: ")
        ship_country = input("What is the shipping country: ")
        product_id = input("What is the product id for the item in the order: ")
        while True:
            if(product_id.isdigit()):
                break
            else:
                product_id = input("Invalid product ID, try again:")
        quantity = input("What is the quantity of the item ordered: ")
        while True:
            if(quantity.isdigit()):
                break
            else:
                quantity = input("Invalid quantity, try again:")
        cursor.callproc("AddNewOrder", (customer_id, order_date, ship_date, ship_address, ship_city, ship_postal_code, ship_country, product_id, quantity))
        conn.commit()
        print("New order added successfully.")
    except mysql.connector.Error as e:
        print(f"Error adding new order: {e}")

def main():
    print(sys.path)
    conn = connect_to_database()
    if conn:
        while True:
            print("\nOptions:")
            option = input("Select an option: ")
            if option == '1':
                list_out_of_stock_products(conn)
            elif option == '2':
                total_orders_per_customer(conn)
            elif option == '3':
                most_expensive_products_in_each_order(conn)
            elif option == '4':
                products_never_ordered(conn)
            elif option == '5':
                total_revenue_by_supplier(conn)
            elif option == '6':
                add_new_order(conn)
            elif option == '7':
                print("Exiting the application.")
                break
            else:
                print("Invalid option. Please choose a valid option.")
        # Close the connection
        conn.close()

if __name__ == "__main__":
    main()
