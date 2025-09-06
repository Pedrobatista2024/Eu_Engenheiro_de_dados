#Atividade 3/9: Armazenamento e Geração de Relatório Simples
#A equipe de analistas precisa que os dados que você coletou e enriqueceu estejam em um formato de fácil acesso para que eles possam começar a construir seus relatórios.
#
#Tarefa:
#
#Armazenamento: Salve o DataFrame final (o que contém o preço, a data e a variação diária) em um arquivo no formato CSV. O nome do arquivo deve ser dados_bitcoin_analise.csv.
#
#Relatório Simples: Crie um pequeno relatório em formato de texto. Este relatório não precisa ser complexo, apenas summarize as descobertas que você já me passou:
#
#Qual a criptomoeda?
#
#Preço mínimo e máximo no período.
#
#Data do preço máximo.
#
#Maior variação diária positiva e a data em que ocorreu.

import requests
import pandas as pd

cripto = 'bitcoin'

url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=brl&days=365'

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

        minimo = tabela_precos['preco'].min().round(2)
        maximo = tabela_precos['preco'].max().round(2)
        data_maximo = tabela_precos.loc[tabela_precos['preco'].idxmax(), 'data']
        max_variacao_diaria = tabela_precos['variacao_diaria'].max()
        dt_max_var_diaria = tabela_precos.loc[tabela_precos['variacao_diaria'].idxmax(), 'data']

        try:
            tabela_precos.to_csv('dados_bitcoin_analise.csv', index=False)
            print("DataFrame salvo com sucesso em 'dados_bitcoin_analise.csv'")
        except:
            print(f'Erro ao criar o Arquivo CSV')

        try:
            texto = f"""Relatório de Análise Preliminar de Criptomoedas
                                   
Criptomoeda: {cripto}
Preço Mínimo no Período: R$ {minimo:,.2f}
Preço Máximo no Período: R$ {maximo:,.2f}
Data do Preço Máximo: {data_maximo}
Maior Variação Diária Positiva: {max_variacao_diaria:,.2f}%
Data da Maior Variação: {dt_max_var_diaria} """

            with open('relatorio_bitcoin.txt', 'w', encoding='utf-8') as arquivo:
                arquivo.write(texto)
            print("Relatório de Análise Preliminar de Criptomoedas Criado com Sucesso")
        except:
            print(f'Erro ao Criar o Relatório de Análise Preliminar de Criptomoedas')
              
    

    else:
        print(f'Erro na requisição: {response.status_code}')

except requests.exceptions.RequestException as e:
    print(f'ocorreu um erro {e}')

