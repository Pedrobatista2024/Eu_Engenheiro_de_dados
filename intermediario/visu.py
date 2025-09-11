import pandas as pd

df = pd.read_parquet('dados_combinados.parquet')

print(df.head(10))