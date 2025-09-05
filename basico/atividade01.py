#Tarefa:
#
#Escolha uma criptomoeda de sua preferência (Bitcoin, Ethereum, etc.).
#
#Utilize uma API gratuita para coletar dados históricos de preço (pelo menos dos últimos 30 dias). Recomendo a CoinGecko API ou a CoinAPI, que oferecem planos gratuitos e são amplamente utilizadas.
#
#Coleta de Dados: Colete dados sobre o preço de fechamento diário. Se possível, inclua outras informações como volume de negociação.
#
#Análise Preliminar: Após coletar os dados, faça uma análise inicial. Não precisa ser algo complexo. Apenas me diga:
#
#Qual a criptomoeda escolhida?
#
#Qual foi o preço mínimo e máximo de fechamento no período?
#
#Qual foi a data do preço máximo?

import requests
import pandas as pd

cripto = 'bitcoin'

url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=brl&days=30'

try:

    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()

        tabela_precos = pd.DataFrame(dados['prices'], columns=['timestamp', 'preco'])
        tabela_precos['data'] = pd.to_datetime(tabela_precos['timestamp'], unit='ms')

        minimo = tabela_precos['preco'].min().round(2)
        maximo = tabela_precos['preco'].max().round(2)
        data_maximo = tabela_precos.loc[tabela_precos['preco'].idxmax(), 'data']

        print(f'A cripto moeda escolhida foi o {cripto}')

        print(f'O preço minimo foi R${minimo} e o preço maximo foi R${maximo}')

        print(f'A data do preço maximo registado: {data_maximo}')
    else:
        print(f'Erro na requisição: {response.status_code}')

except requests.exceptions.RequestException as e:
    print(f'ocorreu um erro {e}')







