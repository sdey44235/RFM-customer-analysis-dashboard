from datetime import datetime
import pandas as pd  # pip install pandas
import numpy as np

data_type = {
    '_CustomerID': str
}
sales_data = pd.read_csv('data/sales_data.csv', dtype=data_type, parse_dates=['OrderDate'])
df = sales_data.copy()
# **Mainly this line gives the Profit(not Revenue) because we also deducts Unit Cost 
#df['Profit'] = (df['Unit Price'] - (df['Unit Price'] * df['Discount Applied']) - df['Unit Cost']) * df['Order Quantity']
discount = df["Discount Applied"]
df["Revenue"] = (
    df["Unit Price"] * (1 - discount)
    * df["Order Quantity"]
)

columns = ['OrderNumber', '_CustomerID', 'OrderDate', 'Revenue']
df_dataset = df[columns]

today_date = pd.to_datetime('2021-01-01')   #This is recent order date in my dataset
rfm_dataset = df_dataset.groupby('_CustomerID').agg({
    'OrderDate': lambda v: (today_date - v.max()).days,
    'OrderNumber': 'nunique',
    'Revenue': 'sum'
})

rfm_dataset.rename(
    columns={
        'OrderDate': 'recency',
        'OrderNumber': 'frequency',
        'Revenue': 'monetory'
    },
    inplace=True
)
#Traditional RFM analysis uses:
# R — Recency: How recently the customer purchased.
# F — Frequency: How often the customer purchases.
# M — Monetary: How much the customer spends.
r= pd.qcut(rfm_dataset['recency'], q=5, labels=range(5, 0, -1))   #here higher the number limit
f= pd.qcut(rfm_dataset['frequency'], q=5, labels=range(1, 6))
m= pd.qcut(rfm_dataset['monetory'], q=5, labels=range(1, 6))

rfm = rfm_dataset.assign(
    R=r.values, 
    F=f.values, 
    M=m.values)
rfm['rfm_score_total'] = rfm[['R', 'F', 'M']].sum(axis=1)

print(rfm.to_markdown())