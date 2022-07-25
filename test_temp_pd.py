# test_temp_pandas


import pandas as pd
import numpy as np

Hol=['name', 'chem123', 'alg']

#initialize a dataframe
df = pd.DataFrame(
	[['Amol', 72, 67, 91],
	['Lini', 78, 69, 87],
	['Kiku', 74, 56, 88],
	['Ajit', 54, 76, 78]],
	columns=['name', 'phy', 'chem', 'alg'])	

#get the dataframe columns
cols = df.columns.values.tolist()  

#print the columns
print(cols)

for item_headDB in Hol:
    for i in cols:
        if item_headDB == i :
            print (item_headDB) 