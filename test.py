import pandas as pd



df1 = pd.read_csv('TxAntennaDAB.csv')

df2 = pd.read_csv('TxParamsDAB.csv', encoding="latin-1")

# print(df)
print(df2)