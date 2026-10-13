import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE / "output"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA / "sales_raw.csv")
print("Raw shape:", df.shape)
print("\nMissing values:\n", df.isnull().sum())
print("\nDuplicate rows:", df.duplicated().sum())

# Data cleaning
df["Category"] = df["Category"].replace({
    "electronics": "Electronics",
    "Electronic": "Electronics"
})
df["Region"] = df["Region"].fillna("Unknown")
df["Date"] = pd.to_datetime(df["Date"])
df = df.drop_duplicates()
df["Sales"] = df["Quantity"] * df["Unit_Price"]
df["Profit_Margin"] = (df["Profit"] / df["Sales"] * 100).round(2)

df.to_csv(DATA / "sales_cleaned.csv", index=False)

# KPIs
print("\n--- KPIs ---")
print("Total Sales:", round(df["Sales"].sum(), 2))
print("Total Profit:", round(df["Profit"].sum(), 2))
print("Total Orders:", df["Order_ID"].nunique())
print("Average Order Value:", round(df["Sales"].mean(), 2))

# Analysis
category_sales = df.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
region_sales = df.groupby("Region", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
top_products = df.groupby("Product", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False).head(10)
monthly_sales = df.assign(Month=df["Date"].dt.to_period("M")).groupby("Month", as_index=False)["Sales"].sum()
monthly_sales["Month"] = monthly_sales["Month"].astype(str)

print("\nSales by category:\n", category_sales)
print("\nSales by region:\n", region_sales)
print("\nTop products:\n", top_products)

# Charts
plt.figure(figsize=(9,5))
plt.bar(category_sales["Category"], category_sales["Sales"])
plt.title("Sales by Category")
plt.xlabel("Category"); plt.ylabel("Sales")
plt.xticks(rotation=20); plt.tight_layout()
plt.savefig(OUT / "sales_by_category.png", dpi=150); plt.close()

plt.figure(figsize=(9,5))
plt.plot(monthly_sales["Month"], monthly_sales["Sales"], marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month"); plt.ylabel("Sales")
plt.xticks(rotation=45); plt.tight_layout()
plt.savefig(OUT / "monthly_sales_trend.png", dpi=150); plt.close()

plt.figure(figsize=(9,5))
plt.barh(top_products["Product"], top_products["Sales"])
plt.title("Top 10 Products by Sales")
plt.xlabel("Sales"); plt.tight_layout()
plt.savefig(OUT / "top_products.png", dpi=150); plt.close()

print("\nDone. Check the output folder for charts.")
