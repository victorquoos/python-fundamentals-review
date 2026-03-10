import pandas as pd
from pathlib import Path


DIR = Path(__file__).parent


orders = pd.read_csv(DIR / "olist_orders_dataset.csv")
items = pd.read_csv(DIR / "olist_order_items_dataset.csv")
df = items.merge(orders, on="order_id")
df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
df["order_approved_at"] = pd.to_datetime(df["order_approved_at"])
df["order_delivered_carrier_date"] = pd.to_datetime(df["order_delivered_carrier_date"])
df["order_delivered_customer_date"] = pd.to_datetime(df["order_delivered_customer_date"])
df["order_estimated_delivery_date"] = pd.to_datetime(df["order_estimated_delivery_date"])


if __name__ == "__main__":
    print(df.head())
    print(df.info())
