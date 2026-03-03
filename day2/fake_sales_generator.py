import random
from datetime import datetime, timedelta
from randomtimestamp import randomtimestamp

CUSTOMERS = [
    "A001", "A002", "A003", "A004",
    "B001", "B002", "B003", "B004",
    "C001", "C002", "C003", "C004",
    "D001", "D002", "D003", "D004",
]

PRODUCTS = [
    ("T-Shirt", "Clothing", 49.90),
    ("Sneakers", "Shoes", 199.90),
    ("Backpack", "Accessories", 89.90),
    ("Jeans", "Clothing", 79.50),
    ("Smartphone", "Electronics", 899.00),
    ("Coffee Maker", "Home", 120.00),
    ("Running Shorts", "Clothing", 35.00),
    ("Bluetooth Speaker", "Electronics", 55.25),
    ("Laptop Sleeve", "Accessories", 29.99),
    ("Desk Lamp", "Home", 45.00),
    ("Yoga Mat", "Fitness", 40.00),
    ("Water Bottle", "Accessories", 25.00)
]

PRICE_VARIATION = 0.1


def get_random_timestamp(since_year=2025) -> str:
    """
    Returns a random YYYY-MM-DD HH:MM:SS string from start_year to now.
    """
    start_date = int(datetime(year=since_year, month=1, day=1).timestamp())
    now = int(datetime.now().timestamp())

    random_seconds = random.randrange(start_date, now)
    random_datetime = datetime.fromtimestamp(random_seconds)
    formated_date = random_datetime.strftime("%Y-%m-%d %H:%M:%S")

    return formated_date


def generate_random_sale() -> dict:
    """
    Simulates a retail transaction with randomized attributes
    """
    customer_id = random.choice(CUSTOMERS)
    product = random.choice(PRODUCTS)
    random_variation = 1 + (random.uniform(-PRICE_VARIATION, PRICE_VARIATION))
    random_date = get_random_timestamp()

    sale = {
        "customer_id": customer_id,
        "product_name": product[0],
        "category": product[1],
        "price": product[2] * random_variation,
        "date": random_date
    }

    return sale


if __name__ == "__main__":
    random_sales = []
    for i in range(200):
        random_sales.append(generate_random_sale())
    for i in random_sales:
        print(i)
