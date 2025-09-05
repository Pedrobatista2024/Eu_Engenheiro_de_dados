#Atividade 2/9: Limpeza e Enriquecimento de Dados
#A base de dados que você coletou está em um estado "bruto". A próxima etapa de um pipeline de dados é a limpeza e, se necessário, o enriquecimento desses dados.
#
#Tarefa:
#
#Limpeza: Verifique se há valores nulos ou faltantes na base de dados que você coletou. Se encontrar, remova-os ou os preencha de forma apropriada. (A CoinGecko geralmente retorna dados completos, mas a verificação é uma boa prática).
#
#Enriquecimento: Adicione uma nova coluna ao seu DataFrame chamada variacao_diaria.
#
#Para cada linha, esta nova coluna deve conter o valor da variação percentual do preço de fechamento em relação ao dia anterior.
#
#Análise Final: Com a nova coluna adicionada, me responda:
#
#Qual foi a maior variação diária positiva (maior alta) no período?
#
#Em qual data essa variação ocorreu?

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

        for coluna in tabela_precos.columns:
            if tabela_precos[coluna].isnull().any():
                print(f'tratando dados nulos da coluna {coluna}')
                tabela_precos[coluna].fillna(method='ffill')
        else:
            print(f'Não há dados nulos no dataframe')
        
        tabela_precos['variacao_diaria'] = ((tabela_precos['preco'] - tabela_precos['preco'].shift(1)) / tabela_precos['preco'].shift(1)) * 100
        
        tabela_precos['variacao_diaria'] = tabela_precos['variacao_diaria'].fillna(0)
        
        max_variacao_diaria = tabela_precos['variacao_diaria'].max()
        dt_max_var_diaria = tabela_precos.loc[tabela_precos['variacao_diaria'].idxmax(), 'data']


        print(f'A maior variação diaria foi {max_variacao_diaria} e ocorreu em {dt_max_var_diaria}')

    else:
        print(f'Erro na requisição: {response.status_code}')

except requests.exceptions.RequestException as e:
    print(f'ocorreu um erro {e}')

