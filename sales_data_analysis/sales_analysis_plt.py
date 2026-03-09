import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
FILENAME = SCRIPT_DIR / "sales.csv"
TIMEFORMAT = "%Y-%m-%d %H:%M:%S"


df = pd.read_csv(FILENAME)
df["date"] = pd.to_datetime(df["date"])


# revenue per month
revenue_per_month = df.groupby(df["date"].dt.to_period("M"))["price"].sum()
revenue_per_month.plot(kind="bar")

plt.title("Revenue per Month")
plt.xlabel("Month")
plt.xticks(rotation=45)
plt.ylabel("Revenue")
plt.tight_layout()

plt.show()


# revenue per category
revenue_per_category = df.groupby("category")["price"].sum().sort_values(ascending=False)
revenue_per_category.plot(kind="pie", autopct="%1.1f%%")

plt.title("Revenue per Category")
plt.xlabel("Category")
plt.ylabel("Revenue")
plt.tight_layout()

plt.show()


# sales per categories
sales_per_category = df["category"].value_counts().sort_values(ascending=False)
sales_per_category.plot(kind="bar")

plt.title("Sales per Category")
plt.xlabel("Category")
plt.ylabel("Number of Sales")
plt.tight_layout()

plt.show()


# top 5 products by revenue
top_products_revenue = df.groupby("product_name")["price"].sum().sort_values(ascending=False).head(5)
top_products_revenue.plot(kind="bar")

plt.title("Top 5 Products by Revenue")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.tight_layout()

plt.show()


# top 5 products by purchases
top_products_purchases = df["product_name"].value_counts().sort_values(ascending=False).head(5)
top_products_purchases.plot(kind="bar")

plt.title("Top 5 Products by Purchases")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.tight_layout()

plt.show()


# top 5 customers by revenue
top_customers_revenue = df.groupby("customer_id")["price"].sum().sort_values(ascending=False).head(5)
top_customers_revenue.plot(kind="bar")

plt.title("Top 5 Customers by Revenue")
plt.xlabel("Customer ID")
plt.ylabel("Revenue")
plt.tight_layout()

plt.show()


# top 5 customers by purchases
top_customers_purchases = df["customer_id"].value_counts().sort_values(ascending=False).head(5)
top_customers_purchases.plot(kind="bar")

plt.title("Top 5 Customer by Puchases")
plt.xlabel("Customer ID")
plt.ylabel("Puchases Number")
plt.tight_layout()

plt.show()


# revenue per weekday
revenue_per_weekday = df.groupby(df["date"].dt.strftime("%a"))["price"].sum()
day_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
revenue_per_weekday = revenue_per_weekday.reindex(day_order)
revenue_per_weekday.plot(kind="bar")

plt.title("Revenue per Weekday")
plt.xlabel("Weekday")
plt.ylabel("Revenue")
plt.tight_layout()

plt.show()


# lowest and highest price per product
extreme_sales = df.groupby("product_name")["price"].agg(["min", "max"])
extreme_sales.columns = ["Lowest Price", "Highest Price"]
extreme_sales.plot(kind="bar")

plt.title("Lowest and Highest Price per Product")
plt.xlabel("Product")
plt.ylabel("Revenue Price")
plt.tight_layout()

plt.show()
