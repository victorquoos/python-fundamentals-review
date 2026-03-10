from data_loader import df
import pandas as pd
import matplotlib.pyplot as plt


# How many orders exist?
print()
unique_orders = df["order_id"].nunique()
print("Unique values:", unique_orders)

# What is the average order value?
print()
average_value = df.groupby("order_id")["price"].sum().mean()
print("Average value per order:", average_value)

# Which products generate the most revenue?
print()
top_products = df.groupby("product_id")["price"].sum().sort_values(ascending=False).head(10)
print("Top products:\n", top_products)

# Which months have more orders?
print()
top_selling_months = df.groupby(df["order_purchase_timestamp"].dt.to_period("M"))["order_id"].nunique().sort_values(ascending=False)
print("Top selling months:\n", top_selling_months.head())

# What is the average delivery time?
print()
df["delivery_time_in_days"] = (df["order_delivered_customer_date"] - df["order_purchase_timestamp"]).dt.total_seconds() / (24 * 3600)
average_delivery_time = df.drop_duplicates(subset=["order_id"])["delivery_time_in_days"].mean()
print("Average delivery time in days:", average_delivery_time)
