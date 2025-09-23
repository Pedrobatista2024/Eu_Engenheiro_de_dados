import requests
import pandas as pd
from bs4 import BeautifulSoup
pd.set_option('display.float_format', '{:.0f}'.format)

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
    
def limpar_valor(valor_texto):
    if isinstance(valor_texto, str):
        return float(valor_texto.replace('$', '').replace(',', ''))
    return valor_texto

df_final = pd.DataFrame(dados_criptos)

df_final['preco'] = df_final['preco'].apply(limpar_valor)
df_final['market_cap'] = df_final['market_cap'].str[-15:].apply(limpar_valor)
df_final['volume_24h'] = df_final['volume_24h'].str[:-1].apply(limpar_valor)

print(df_final)