import sqlite3
import pandas as pd


NOME_DO_ARQUIVO_SQLITE = 'rickandmorty_analise.db'

conn = sqlite3.connect(NOME_DO_ARQUIVO_SQLITE)
print("\n--- Tabela: Personagens (Amostra) ---")

query_personagens = "SELECT * FROM personagens LIMIT 5"
df_personagens = pd.read_sql_query(query_personagens, conn)
print(df_personagens)

print("\n--- Tabela: Localizações (Amostra) ---")

query_localizacoes = "SELECT * FROM localizacoes"
df_localizacoes = pd.read_sql_query(query_localizacoes, conn)
print(df_localizacoes.head()) 

conn.close()