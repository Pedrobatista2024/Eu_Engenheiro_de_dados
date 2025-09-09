#Atividade 4/9: Integração de Dados e Análise de Múltiplas Fontes
#Nossa equipe de analistas agora precisa de uma visão mais ampla, integrando os dados de criptomoedas com informações do mercado financeiro tradicional.
#
#Tarefa:
#
#Coleta de Dados Adicionais: Use uma API para coletar dados históricos (dos últimos 30 dias) do S&P 500 (^GSPC) ou de qualquer outro índice de mercado que você prefira. Uma ótima opção para isso é a API gratuita do Yahoo Finance (pode usar bibliotecas como yfinance para facilitar).
#
#Integração: Combine o DataFrame de dados de criptomoeda (Bitcoin) que você já tem com este novo DataFrame do índice financeiro.
#
#O objetivo é ter um único DataFrame que contenha o preço do Bitcoin e o preço do S&P 500 para cada data correspondente.
#
#Você precisará garantir que as datas de ambos os DataFrames estejam alinhadas antes de fazer a união. Considere que pode haver datas em que o mercado de ações está fechado (fins de semana, feriados), mas o mercado de criptomoedas está aberto.
#
#Análise de Correlação: Calcule o coeficiente de correlação de Pearson entre o preço do Bitcoin e o preço do S&P 500 no período. Este coeficiente mede a força e a direção de uma relação linear entre duas variáveis. O valor varia de -1 (correlação negativa) a +1 (correlação positiva).
#
#Para me entregar, envie o código que realiza a coleta e a união dos dados, e também me diga:
#
#Qual o valor do coeficiente de correlação?
#
#O que esse valor significa para a relação entre o preço do Bitcoin e o S&P 500 no período analisado?

import yfinance as yf
import pandas as pd

pd.set_option('display.max_columns', None)


dados_sp500 = yf.download('^GSPC', period='30d')


print(dados_sp500.head())

dados_sp500 = dados_sp500['Close'].reset_index()
print(dados_sp500.head())

dados_sp500 = dados_sp500.rename(columns={'Close': 'preco_sp500', 'Date': 'data'})

print(dados_sp500.head())


dados_bitcoin = pd.read_csv('../basico/dados_bitcoin_analise.csv')

dados_bitcoin['data'] = pd.to_datetime(dados_bitcoin['data']).dt.date
dados_bitcoin['data'] = pd.to_datetime(dados_bitcoin['data'])

dados_bitcoin_diario = dados_bitcoin.groupby('data')['preco'].mean().reset_index()

dados_bitcoin = dados_bitcoin.reset_index()


df_combinado = pd.merge(dados_bitcoin_diario[['data', 'preco']], dados_sp500, on='data', how='inner')

df_combinado.to_csv('dados_combinados.csv', index=False)

matriz_correlacao = df_combinado[['preco', '^GSPC']].corr()

print(matriz_correlacao)

correlacao = matriz_correlacao.loc['preco', '^GSPC']#

print(f'''O Coeficiente de correlação é : {correlacao:.4f}
oque indica que eles se movem em direções opostas''')