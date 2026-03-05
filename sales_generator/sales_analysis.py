import pandas as pd
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
FILENAME = SCRIPT_DIR / "sales.csv"
TIMEFORMAT = "%Y-%m-%d %H:%M:%S"


df = pd.read_csv(FILENAME)
df["date"] = pd.to_datetime(df["date"])

print(df.head())
print(df.info())

print("\n=== Top product by revenue =======================")
revenue_by_product = df.groupby("product_name")["price"].sum().sort_values(ascending=False)
top_product = revenue_by_product.idxmax()
print(f"{top_product}: ${revenue_by_product[top_product]:.2f}")

print("\n=== Top category by sales count ==================")
sellings_per_category = df["category"].value_counts().sort_values(ascending=False)
top_category = sellings_per_category.idxmax()
print(f"{top_category}: {sellings_per_category[top_category]}")

print("\n=== Top customer by revenue ======================")
revenue_by_customer = df.groupby("customer_id")["price"].sum().sort_values(ascending=False)
top_customer = revenue_by_customer.idxmax()
print(f"{top_customer}: ${revenue_by_customer[top_customer]:.2f}")

print("\n=== Top 3 customers ==============================")
top_customers = revenue_by_customer.sort_values(ascending=False).head(3)
for customer, revenue in top_customers.items():
    print(f"{customer}: ${revenue:.2f}")

print("\n=== Biggest sale =================================")
top_sale = df["price"].idxmax()
print(df.loc[top_sale])

print("\n=== Best and worst months ========================")
revenue_per_month = df.groupby(df["date"].dt.to_period("M"))["price"].sum()
best_month = revenue_per_month.idxmax()
worst_month = revenue_per_month.idxmin()
print(f"Best month: {best_month} (${revenue_per_month[best_month]:.2f})")
print(f"Worst month: {worst_month} (${revenue_per_month[worst_month]:.2f})")

print("\n=== Best category share ==========================")
category_revenue = df.groupby("category")["price"].sum()
top_category = category_revenue.idxmax()
share = (category_revenue[top_category] / df["price"].sum()) * 100
print(f"{top_category} represents {share:.1f}% of revenue")

print("\n=== Average order value per customer =============")
average_per_customer = df.groupby("customer_id")["price"].agg(["mean", "count"])
average_per_customer.columns = ["average_price", "total_orders"]
average_per_customer = average_per_customer.sort_values(by="average_price", ascending=False)
for customer_id, row in average_per_customer.iterrows():
    avg_price = row["average_price"]
    total_orders = row["total_orders"]
    print(f"Customer {customer_id:<6}: {total_orders:>4.0f} orders | Avg Spend: ${avg_price:<8.2f}")

print("\n=== Revenue per weekday ==========================")
revenue_per_weekday = df.groupby(df["date"].dt.strftime("%a"))["price"].sum()
# Adjust the pd series to show the weekday list in the ordar that I want
day_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
revenue_per_weekday = revenue_per_weekday.reindex(day_order)
for day, total in revenue_per_weekday.items():
    print(f"{day:<5} | ${total:>9.2f}")

print("=== Most popular product per category ==============")
most_pop_per_category = df.groupby("category")["product_name"].value_counts().groupby(level=0).head(1)
print(most_pop_per_category)

print("=== Customer with the most purchases ===============")
most_purchases_customer = df["customer_id"].value_counts().head(1)
print(most_purchases_customer)

print("=== Smallest and biggest price per product =========")
extreme_sales = df.groupby("product_name")["price"].agg(["min", "max"])
print(extreme_sales)
