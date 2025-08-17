import sqlite3

conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    product_id INTEGER,
    status TEXT DEFAULT 'Processing',
    FOREIGN KEY(customer_id) REFERENCES customers(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
)
''')

conn.commit()


def add_customer(name):
    cursor.execute("INSERT INTO customers (name) VALUES (?)", (name,))
    conn.commit()
    print(f" Customer '{name}' added.")

def add_product(name, price):
    cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
    conn.commit()
    print(f" Product '{name}' added at ${price:.2f}.")

def place_order(customer_id, product_id):
    cursor.execute("INSERT INTO orders (customer_id, product_id) VALUES (?, ?)", (customer_id, product_id))
    conn.commit()
    print(" Order placed successfully.")

def view_orders():
    cursor.execute('''
    SELECT orders.id, customers.name, products.name, products.price, orders.status
    FROM orders
    JOIN customers ON orders.customer_id = customers.id
    JOIN products ON orders.product_id = products.id
    ''')
    orders = cursor.fetchall()
    
    print("\n--- All Orders ---")
    for o in orders:
        print(f"Order ID: {o[0]}, Customer: {o[1]}, Product: {o[2]}, Price: ${o[3]:.2f}, Status: {o[4]}")

def view_customers():
    cursor.execute("SELECT * FROM customers")
    for row in cursor.fetchall():
        print(row)

def view_products():
    cursor.execute("SELECT * FROM products")
    for row in cursor.fetchall():
        print(row)


def main():
    while True:
        print("\n====== E-commerce Order Tracking ======")
        print("1. Add Customer")
        print("2. Add Product")
        print("3. Place Order")
        print("4. View Orders")
        print("5. View Customers")
        print("6. View Products")
        print("0. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Enter customer name: ")
            add_customer(name)

        elif choice == '2':
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            add_product(name, price)

        elif choice == '3':
            view_customers()
            customer_id = int(input("Enter customer ID: "))
            view_products()
            product_id = int(input("Enter product ID: "))
            place_order(customer_id, product_id)

        elif choice == '4':
            view_orders()

        elif choice == '5':
            view_customers()

        elif choice == '6':
            view_products()

        elif choice == '0':
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")

    conn.close()

if __name__ == "__main__":
    main()


  