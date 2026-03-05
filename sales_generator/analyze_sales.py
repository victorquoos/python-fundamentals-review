from datetime import datetime
import csv
from pathlib import Path
from collections import defaultdict


SCRIPT_DIR = Path(__file__).parent
FILENAME = SCRIPT_DIR / 'sales.csv'
TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

COST_PERCENT = 0.65


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


def calculate_profit(value: float, cost_percent=COST_PERCENT) -> float:
    """
    Returns the profit of some value based on cost percent
    """
    return value - (value * cost_percent)


def calculate_profit_per_category(revenue_per_category: dict[str, float]) -> dict[str, float]:
    """
    Returns the profit per category based on the cost percent
    """
    profit = {category: calculate_profit(revenue)
              for category, revenue in revenue_per_category.items()}

    profit = dict(sorted(profit.items(), key=lambda x: x[1], reverse=True))

    return profit


if __name__ == "__main__":
    sales_data = get_sales_data()

    total_revenue = compute_total_revenue(sales_data)
    revenue_per_category = compute_revenue_per_category(sales_data)
    top_product = compute_top_product(sales_data)
    revenue_per_month = compute_revenue_per_month(sales_data)

    best_month = max(revenue_per_month.items(), key=lambda x: x[1])
    worst_month = min(revenue_per_month.items(), key=lambda x: x[1])
    top_category = max(revenue_per_category.items(), key=lambda x: x[1])
    top_category_proportion = (top_category[1] / total_revenue) * 100

    total_profit = calculate_profit(total_revenue)
    profit_per_category = calculate_profit_per_category(revenue_per_category)

    print("=== Business Insight ===")
    print(f"The best month was {best_month[0]}, with a total revenue of ${best_month[1]:.2f}")
    print(f"The worst month was {worst_month[0]}, with a total revenue of ${worst_month[1]:.2f}")
    print(f"{top_category[0]} represent %{top_category_proportion:.1f} of total revenue. Business is highly dependent on this category")
    print(f"The total profit of all revenues was ${total_profit:.2f}")
    print("------------------------")
    print("Profit per category")
    for c, p in profit_per_category.items():
        print(f"{c:<15} ${p:>.2f}")
    print("========================")
