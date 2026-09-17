from pathlib import Path
from datetime import date,timedelta
import random
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/"data"/"raw"; OUT.mkdir(parents=True,exist_ok=True)
random.seed(21)
customers=pd.DataFrame([[i,f"Cliente {i:03d}",random.choice(["SP","RJ","MG","PR"])] for i in range(1,101)],columns=["customer_id","customer_name","state"])
products=pd.DataFrame([[i,f"SKU-{i:03d}",random.choice(["Tech","Casa","Moda","Esporte"]),round(random.uniform(20,800),2)] for i in range(1,41)],columns=["product_id","product_name","category","list_price"])
rows=[]; start=date(2025,1,1)
for sale_id in range(1,1801):
    p=products.sample(1,random_state=sale_id).iloc[0]; qty=random.randint(1,4); discount=random.choice([0,0,.05,.1,.15])
    rows.append([sale_id,random.randint(1,100),int(p.product_id),(start+timedelta(days=random.randint(0,610))).isoformat(),random.choice(["Web","App","Loja"]),qty,float(p.list_price),discount])
customers.to_csv(OUT/"customers.csv",index=False); products.to_csv(OUT/"products.csv",index=False)
pd.DataFrame(rows,columns=["sale_id","customer_id","product_id","sale_date","channel","quantity","unit_price","discount_pct"]).to_csv(OUT/"sales.csv",index=False)
