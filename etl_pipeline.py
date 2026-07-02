"""
ETL Pipeline - Bluestock MF Capstone
Author: Aman Karwal
Date: July 2026
"""

import pandas as pd
import numpy as np
import sqlite3
import os
import warnings
warnings.filterwarnings("ignore")

CSV  = r"C:\Users\Aman Karwal\Downloads\bluestock-mf-capstone\\"
BASE = r"C:\Users\Aman Karwal\bluestock_mf_capstone\\"
DB   = BASE + "bluestock_mf.db"
SAVE = CSV + "processed\\"
os.makedirs(SAVE, exist_ok=True)

print("=" * 50)
print("BLUESTOCK MF - ETL PIPELINE")
print("=" * 50)

print("\n[1/3] EXTRACTING...")
try:
    fund_master  = pd.read_csv(CSV + "01_fund_master.csv")
    nav_history  = pd.read_csv(CSV + "02_nav_history.csv")
    aum          = pd.read_csv(CSV + "03_aum_by_fund_house.csv")
    sip          = pd.read_csv(CSV + "04_monthly_sip_inflows.csv")
    category     = pd.read_csv(CSV + "05_category_inflows.csv")
    folio        = pd.read_csv(CSV + "06_industry_folio_count.csv")
    performance  = pd.read_csv(CSV + "07_scheme_performance.csv")
    transactions = pd.read_csv(CSV + "08_investor_transactions.csv")
    holdings     = pd.read_csv(CSV + "09_portfolio_holdings.csv")
    benchmark    = pd.read_csv(CSV + "10_benchmark_indices.csv")
    print("  All 10 datasets loaded!")
except FileNotFoundError as e:
    print(f"  ERROR: {e}")
    exit(1)

print("\n[2/3] TRANSFORMING...")
nav_history["date"] = pd.to_datetime(nav_history["date"])
nav_history = nav_history.sort_values(["amfi_code","date"])
nav_history = nav_history.drop_duplicates(subset=["amfi_code","date"])
nav_history = nav_history[nav_history["nav"] > 0]

nav_filled = []
for code, group in nav_history.groupby("amfi_code"):
    group = group.set_index("date")
    group = group.resample("B").ffill()
    group["amfi_code"] = code
    group = group.reset_index()
    nav_filled.append(group)
nav_clean = pd.concat(nav_filled, ignore_index=True)
print(f"  NAV: {len(nav_clean):,} rows")

transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"])
transactions_clean = transactions.dropna(subset=["investor_id","amount_inr","transaction_type"])
transactions_clean = transactions_clean[transactions_clean["amount_inr"] > 0]
print(f"  Transactions: {len(transactions_clean):,} rows")

sip["month"] = pd.to_datetime(sip["month"])
sip_clean = sip.ffill()
aum["date"] = pd.to_datetime(aum["date"])
benchmark["date"] = pd.to_datetime(benchmark["date"])

nav_clean.to_csv(SAVE + "clean_nav.csv", index=False)
transactions_clean.to_csv(SAVE + "clean_transactions.csv", index=False)
sip_clean.to_csv(SAVE + "clean_sip.csv", index=False)
fund_master.to_csv(SAVE + "clean_fund_master.csv", index=False)
performance.to_csv(SAVE + "clean_performance.csv", index=False)
print("  Processed files saved!")

print("\n[3/3] LOADING INTO DATABASE...")
conn = sqlite3.connect(DB)

fund_master.to_sql("dim_fund",                conn, if_exists="replace", index=False)
nav_clean.to_sql("fact_nav",                  conn, if_exists="replace", index=False)
transactions_clean.to_sql("fact_transactions",conn, if_exists="replace", index=False)
performance.to_sql("fact_performance",        conn, if_exists="replace", index=False)
sip_clean.to_sql("fact_sip",                  conn, if_exists="replace", index=False)
aum.to_sql("fact_aum",                        conn, if_exists="replace", index=False)
category.to_sql("fact_category",              conn, if_exists="replace", index=False)
folio.to_sql("fact_folio",                    conn, if_exists="replace", index=False)
holdings.to_sql("fact_holdings",              conn, if_exists="replace", index=False)
benchmark.to_sql("fact_benchmark",            conn, if_exists="replace", index=False)

tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type=\'table\'", conn)
print(f"  {len(tables)} tables loaded!")
for t in tables["name"]:
    count = pd.read_sql(f"SELECT COUNT(*) as rows FROM {t}", conn)
    print(f"    {t}: {count['rows'][0]:,} rows")

conn.close()
print("\n" + "=" * 50)
print("ETL COMPLETE!")
print("=" * 50)
