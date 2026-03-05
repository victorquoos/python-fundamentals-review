import pandas as pd
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
FILENAME = SCRIPT_DIR / 'sales.csv'
TIMEFORMAT = "%Y-%m-%d %H:%M:%S"


df = pd.read_csv(FILENAME)
df["date"] = pd.to_datetime(df["date"])

print(df.head())
print(df.info())

# print("==========================================")
# print("Total revenue:", df["price"].sum())
# print("Total sales:", len(df))
# print("Average sale:", df["price"].mean())
# print("=== Best selling products ================")
# print(df["product_name"].value_counts())
# print("=== Revenue by category ==================")
# print(df.groupby("category")["price"].sum())
# print("=== Top customers ========================")
# print(df.groupby("customer_id")["price"].sum().sort_values(ascending=False))
# print("==========================================")

print("=== Top product by revenue ===============")
revenue_by_product = df.groupby("product_name")["price"].sum().sort_values(ascending=False)
top_product = revenue_by_product.idxmax()
print(f"{top_product}: ${revenue_by_product[top_product]:.2f}")


print("=== Top category by sales count ==========")
sellings_per_category = df["category"].value_counts().sort_values(ascending=False)
top_category = sellings_per_category.idxmax()
print(f"{top_category}: {sellings_per_category[top_category]}")

print("=== Top Customer by revenue ==============")
revenue_by_customer = df.groupby("customer_id")["price"].sum().sort_values(ascending=False)
top_customer = revenue_by_customer.idxmax()
print(f"{top_customer}: ${revenue_by_customer[top_customer]:.2f}")

print("=== Biggest sale =========================")
top_sale = df["price"].idxmax()
print(df.loc[top_sale])

print("=== Revenue per month ====================")
revenue_per_month = df.groupby(df['date'].dt.to_period('M'))['price'].sum()
for month, revenue in revenue_per_month.items():
    print(f"{month}: ${revenue:.2f}")
