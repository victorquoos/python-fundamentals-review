import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
FILENAME = SCRIPT_DIR / "sales.csv"
TIMEFORMAT = "%Y-%m-%d %H:%M:%S"


df = pd.read_csv(FILENAME)
df["date"] = pd.to_datetime(df["date"])


# Chart 1 - revenue per month
revenue_per_month = df.groupby(df["date"].dt.to_period("M"))["price"].sum()
revenue_per_month.plot(kind="bar")

plt.title("Revenue per Month")
plt.xlabel("Month")
plt.xticks(rotation=45)
plt.ylabel("Revenue")
plt.tight_layout()

plt.show()


# Chart 2 - revenue per category
revenue_per_category = df.groupby("category")["price"].sum().sort_values(ascending=False)
revenue_per_category.plot(kind="bar")

plt.title("Revenue per Category")
plt.xlabel("Category")
plt.ylabel("Revenue")
plt.tight_layout()

plt.show()


# Chart 3 - top 5 products
top_products = df.groupby("product_name")["price"].sum().sort_values(ascending=False).head(5)
top_products.plot(kind="bar")

plt.title("Top 5 Products by Revenue")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.tight_layout()

plt.show()
