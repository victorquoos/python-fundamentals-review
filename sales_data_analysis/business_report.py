import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
SALES_DATA = SCRIPT_DIR / "sales.csv"
SALES_REPORT = SCRIPT_DIR / "report_summary.csv"


df = pd.read_csv(SALES_DATA)
df["date"] = pd.to_datetime(df["date"])


total_revenue = df["price"].sum()
average_revenue = df["price"].mean()

sales_by_category = df["category"].value_counts().sort_values(ascending=False)
revenue_by_category = df.groupby("category")["price"].sum().sort_values(ascending=False)
average_price_by_category = df.groupby("category")["price"].mean().sort_values(ascending=False)

sales_by_customer = df["customer_id"].value_counts().sort_values(ascending=False)
revenue_by_customer = df.groupby("customer_id")["price"].sum().sort_values(ascending=False)
average_price_by_customer = df.groupby("customer_id")["price"].mean().sort_values(ascending=False)

sales_by_product = df["product_name"].value_counts().sort_values(ascending=False)
revenue_by_product = df.groupby("product_name")["price"].sum().sort_values(ascending=False)
average_price_by_product = df.groupby("product_name")["price"].mean().sort_values(ascending=False)

revenue_by_weekday = df.groupby(df["date"].dt.day_of_week)["price"].sum()
days = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
revenue_by_weekday.index = revenue_by_weekday.index.map(days)
revenue_by_month = df.groupby(df["date"].dt.to_period("M"))["price"].sum()

#

print("Total revenue:", round(total_revenue, 2))
print("Average order value:", round(average_revenue, 2))
print("Total number of sales", len(df))
top_5_customers = list(sales_by_customer.head(5).keys())
print("Top 5 customers:", top_5_customers)

best_month = revenue_by_month.idxmax()
worst_month = revenue_by_month.idxmin()
print("Best month:", best_month)
print("Worst month:", worst_month)

revenue_by_month.plot(kind="line")
plt.title("Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()

revenue_by_category.plot(kind="bar")
plt.title("Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()

#

metrics = {
    "total_revenue": round(total_revenue),
    "total_sales": len(df),
    "average_revenue": round(average_revenue),
    "best_month": best_month,
    "worst_month": worst_month,
    "top_customers": top_5_customers
}

metrics_df = pd.DataFrame(metrics.items(), columns=["metric", "value"])
metrics_df.to_csv(SALES_REPORT, index=False)
