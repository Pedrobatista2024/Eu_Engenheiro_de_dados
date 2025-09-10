import yfinance as yf
import pandas as pd
import os
import requests
from datetime import date, timedelta

pd.set_option('display.max_columns', None)

ontem = date.today() - timedelta(days=1)
hoje = date.today()

try:
    dados_sp500_novos = yf.download('^GSPC', start=ontem, end=hoje)

    dados_sp500_novos = dados_sp500_novos['Close'].reset_index()
    dados_sp500_novos = dados_sp500_novos.rename(columns={'Close': 'preco_sp500', 'Date': 'data'})
except:
    print('erro ao extrair dados da sp500')


data_formatada = ontem.strftime('%d-%m-%Y')

url = f'https://api.coingecko.com/api/v3/coins/bitcoin/history?date={data_formatada}&localization=false'

try:

    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()

        preco_bitcoin = dados.get('market_data', {}).get('current_price', {}).get('brl', None)

        if preco_bitcoin is not None:
            dados_bitcoin_novos = pd.DataFrame([{
                'data': pd.to_datetime(ontem),
                'preco': preco_bitcoin
            }])

        else:
            print(f"Dados de preço não encontrados para {ontem}.")
            dados_bitcoin_novos = pd.DataFrame()
    else:
        print(f'Erro na requisição: {response.status_code}')
        dados_bitcoin_novos = pd.DataFrame()


except requests.exceptions.RequestException as e:
    print(f'ocorreu um erro {e}')
    dados_bitcoin_novos = pd.DataFrame()

print(dados_bitcoin_novos)
print('*'*25)
print(dados_sp500_novos.head())








