# backend/db_setup.py

from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///backend/orders.db")

# Use transaction-aware context manager to auto-commit
with engine.begin() as conn:
    conn.execute(text("DROP TABLE IF EXISTS orders"))
    conn.execute(text("DROP TABLE IF EXISTS customers"))
    conn.execute(text("DROP TABLE IF EXISTS products"))

    conn.execute(
        text(
            """
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT,
            city TEXT
        );
    """
        )
    )

    conn.execute(
        text(
            """
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL
        );
    """
        )
    )

    conn.execute(
        text(
            """
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            product_id INTEGER,
            order_date TEXT,
            amount INTEGER,
            FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY(product_id) REFERENCES products(product_id)
        );
    """
        )
    )

    conn.execute(
        text(
            """
        INSERT INTO customers VALUES
        (1, 'Alice', 'Guwahati'),
        (2, 'Bob', 'Delhi');
    """
        )
    )

    conn.execute(
        text(
            """
        INSERT INTO products VALUES
        (1, 'Football', 500),
        (2, 'Shoes', 1500);
    """
        )
    )

    conn.execute(
        text(
            """
        INSERT INTO orders VALUES
        (1, 1, 1, '2024-06-01', 2),
        (2, 2, 2, '2024-06-15', 1),
        (3, 1, 2, '2024-07-01', 3);
    """
        )
    )

print("✅ Database and tables created with sample data!")
