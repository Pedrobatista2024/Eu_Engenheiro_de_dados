#Atividade 7/9: Web Scraping e Extração de Dados Não Estruturados
#Em muitos projetos, os dados que precisamos não estão disponíveis em uma API bem definida. A única forma de obtê-los é extraindo-os diretamente de um site, em um processo conhecido como Web Scraping.
#
#Tarefa:
#
#Escolha um Site: Vá até um site de criptomoedas, como a página principal do CoinMarketCap ou do CoinGecko, e identifique a tabela das principais criptomoedas.
#
#Web Scraping: Utilize uma biblioteca Python (como requests para obter o HTML e Beautiful Soup para analisar) para extrair os dados da tabela. Você deve fazer isso sem usar a API.
#
#Extração de Dados: Extraia os dados das 5 primeiras criptomoedas. Para cada uma, colete as seguintes informações:
#
#Nome da Criptomoeda
#
#Preço
#
#Volume de negociação em 24h
#
#Capitalização de Mercado (Market Cap)
#
#Para a entrega, envie o código que realiza o web scraping e o DataFrame final com os dados extraídos. Não precisa me enviar os dados em um arquivo.

import requests
import pandas as pd
from bs4 import BeautifulSoup
pd.options.display.float_format = '{:,.2f}'.format

url = 'https://coinmarketcap.com/'

try:
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        print('conteúdo HTML obtido com sucesso. você está pronto para o Beautiful Soup.')
    else:
        print(f"Erro ao fazer a requisição. Status code: {response.status_code}")
        print("Verifique se a URL está correta e sua conexão com a internet.")
except requests.exceptions.RequestException as e:
    print(f"Ocorreu um erro de conexão: {e}")

soup = BeautifulSoup(html_content, 'html.parser')

tabela = soup.find('table', class_= 'sc-7e3c705d-3 keBvNC cmc-table')
 
if tabela:
    print("Tabela encontrada. Agora você pode extrair os dados das linhas e colunas.")
    
else:
    print("Atenção: Tabela não encontrada. Verifique a classe ou id no código HTML.")

linhas = tabela.find_all('tr')[1:]

dados_criptos = [] 



for linha in linhas[:5]:
    celulas = linha.find_all('td')
    
    nome_cripto = celulas[2].text.strip()
    preco = celulas[3].text.strip()
    market_cap = celulas[7].text.strip()
    volume_24h = celulas[8].text.strip()

    dados_criptos.append({
        'nome': nome_cripto,
        'preco': preco,
        'market_cap': market_cap,
        'volume_24h': volume_24h
    })
    
def limpar_e_converter_valor(valor_texto):
    if not isinstance(valor_texto, str):
        return valor_texto
    
    valor_limpo = valor_texto.replace('$', '').replace(',', '')
    
    multiplicador = 1
    if 'B' in valor_limpo:
        multiplicador = 1_000_000_000
        valor_limpo = valor_limpo.replace('B', '')
    elif 'M' in valor_limpo:
        multiplicador = 1_000_000
        valor_limpo = valor_limpo.replace('M', '')
    elif 'T' in valor_limpo:
        multiplicador = 1_000_000_000_000
        valor_limpo = valor_limpo.replace('T', '')
    elif 'K' in valor_limpo:
        multiplicador = 1_000
        valor_limpo = valor_limpo.replace('K', '')
        
    try:
        return float(valor_limpo) * multiplicador
    except ValueError:
        
        return None

df_final = pd.DataFrame(dados_criptos)

df_final['preco'] = df_final['preco'].apply(limpar_e_converter_valor)
df_final['market_cap'] = df_final['market_cap'].apply(limpar_e_converter_valor)
df_final['volume_24h'] = df_final['volume_24h'].apply(limpar_e_converter_valor)


print(df_final.dtypes)