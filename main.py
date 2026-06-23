import pandas as pd
from sklearn.preprocessing import StandardScaler as scaler
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
from sqlalchemy import create_engine



df = pd.read_excel('Online Retail.xlsx')
df.dropna(subset=['CustomerID'], inplace=True)
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
rfm = df.groupby('CustomerID', as_index=False).agg({
    'InvoiceDate': 'max',
    'TotalPrice':'sum',
    'InvoiceNo':'nunique'
})

#rfm block that made our df go to rfm (though ofc, we wrote a bit of rfm before)
rfm['Recency'] = (rfm['InvoiceDate'].max() - rfm['InvoiceDate']).dt.days
rfm = rfm[['CustomerID', 'Recency', 'TotalPrice', 'InvoiceNo']]
rfm = rfm.rename(columns={'TotalPrice': 'Monetary', 'InvoiceNo': 'Frequency'})
X=rfm[['Recency', 'Monetary', 'Frequency']]
z=scaler().fit_transform(X)
rfm[['Recency', 'Monetary', 'Frequency']] = z

#here we got our rfm to be kmean-ed 
llist=[]
for k in range(1,11):
    kmeans=KMeans(n_clusters=k)
    kmeans.fit(z)
    llist.append(kmeans.inertia_)
plt.plot(range(1,11),llist)
plt.show()

#main kmean
kmeans=KMeans(n_clusters=4)
kmeans.fit(z)
Cluster=kmeans.labels_
rfm['Cluster'] = Cluster

#converting this kmean-ed rfm to sql 
engine = create_engine("sqlite:///final.db")
rfm.to_sql("finaltable", con=engine, if_exists="replace", index=False)

