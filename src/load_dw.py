from pathlib import Path
import sqlite3
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/"data"/"raw"; OUT=ROOT/"data"/"output"; OUT.mkdir(parents=True,exist_ok=True)
DB=OUT/"ecommerce_dw.db"; SCHEMA=ROOT/"sql"/"schema.sql"

def build_dimensions(customers,products,sales):
    dc=customers.drop_duplicates("customer_id").reset_index(drop=True).copy(); dc.insert(0,"customer_key",range(1,len(dc)+1))
    dp=products[["product_id","product_name","category"]].drop_duplicates("product_id").reset_index(drop=True).copy(); dp.insert(0,"product_key",range(1,len(dp)+1))
    dates=pd.to_datetime(sales.sale_date).drop_duplicates().sort_values().reset_index(drop=True)
    dd=pd.DataFrame({"full_date":dates.dt.strftime("%Y-%m-%d"),"year":dates.dt.year,"quarter":dates.dt.quarter,"month":dates.dt.month,"month_name":dates.dt.month_name(),"day":dates.dt.day,"weekday":dates.dt.weekday})
    dd.insert(0,"date_key",dates.dt.strftime("%Y%m%d").astype(int))
    channels=pd.DataFrame({"channel":sorted(sales.channel.unique())}); channels.insert(0,"channel_key",range(1,len(channels)+1))
    return dc,dp,dd,channels

def make_fact(sales,dc,dp,dd,dch):
    f=sales.copy(); f["sale_date"]=pd.to_datetime(f.sale_date).dt.strftime("%Y-%m-%d")
    f=f.merge(dc[["customer_id","customer_key"]],on="customer_id").merge(dp[["product_id","product_key"]],on="product_id").merge(dd[["full_date","date_key"]],left_on="sale_date",right_on="full_date").merge(dch,on="channel")
    f["gross_amount"]=(f.quantity*f.unit_price).round(2); f["net_amount"]=(f.gross_amount*(1-f.discount_pct)).round(2)
    f=f.reset_index(drop=True); f.insert(0,"sale_key",range(1,len(f)+1))
    return f[["sale_key","sale_id","customer_key","product_key","date_key","channel_key","quantity","unit_price","discount_pct","gross_amount","net_amount"]]

def load(db_path=DB):
    c=pd.read_csv(RAW/"customers.csv"); p=pd.read_csv(RAW/"products.csv"); s=pd.read_csv(RAW/"sales.csv")
    dc,dp,dd,dch=build_dimensions(c,p,s); fact=make_fact(s,dc,dp,dd,dch)
    with sqlite3.connect(db_path) as conn:
        conn.executescript(SCHEMA.read_text(encoding="utf-8"))
        dc.to_sql("dim_customer",conn,if_exists="append",index=False); dp.to_sql("dim_product",conn,if_exists="append",index=False); dd.to_sql("dim_date",conn,if_exists="append",index=False); dch.to_sql("dim_channel",conn,if_exists="append",index=False); fact.to_sql("fact_sales",conn,if_exists="append",index=False)
    return len(fact)
if __name__=="__main__": print("Fact rows loaded:",load())
