from datetime import datetime
import csv
from pathlib import Path
from collections import defaultdict


SCRIPT_DIR = Path(__file__).parent
FILENAME = SCRIPT_DIR / 'sales.csv'
TIMEFORMAT = "%Y-%m-%d %H:%M:%S"


def get_sales_data() -> list[dict]:
    """
    Returns a dictionary with all the data from the sales.csv file.
    """
    if not FILENAME.exists():
        return []

    try:
        with open(FILENAME, 'r') as file:
            reader = csv.DictReader(file)
            data = list(reader)

        for sale in data:
            # Convert the price to float
            if 'price' in sale:
                sale['price'] = float(sale['price'])

            # Convert the date to a datetime object
            if 'date' in sale:
                sale['date'] = datetime.strptime(sale['date'], TIMEFORMAT)

        return data
    except (IOError, ValueError) as e:
        print(f"Error reading expenses file: {e}")
        return []


def compute_total_revenue(data: list[dict]) -> float:
    """
    Returns the sum of all the prices of the products sold in the given sales data.
    """
    total = 0
    for sale in data:
        total += sale['price']

    return total


def compute_revenue_per_category(data: list[dict]) -> dict[str, float]:
    """
    Returns the total revenue per category in the given sales data.
    """
    revenue = defaultdict(float)
    for sale in data:
        revenue[sale['category']] += sale['price']

    return dict(revenue)


def compute_top_product(data: list[dict]) -> tuple[str, float]:
    """
    Calculates the sum of all revenues per product.
    Returns the product with the biggest total revenue.
    """
    revenue = defaultdict(float)
    for sale in data:
        revenue[sale['product_name']] += sale['price']
    top_product = max(revenue.items(), key=lambda x: x[1])
    return top_product


def compute_revenue_per_month(data: list[dict]) -> dict[str, float]:
    """
    Returns the total revenue for each month in the given sales data
    """
    revenue = defaultdict(float)
    for sale in data:
        date = sale['date'].strftime("%Y-%m")
        revenue[date] += sale['price']
    revenue = sorted(revenue.items())
    return dict(revenue)


if __name__ == "__main__":
    sales_data = get_sales_data()

    total_revenue = compute_total_revenue(sales_data)
    print(total_revenue)

    revenue_per_category = compute_revenue_per_category(sales_data)
    print(revenue_per_category)

    top_product = compute_top_product(sales_data)
    print(top_product)

    revenue_per_month = compute_revenue_per_month(sales_data)
    for m, r in revenue_per_month.items():
        print(f"{m} : {r:.2f}")
