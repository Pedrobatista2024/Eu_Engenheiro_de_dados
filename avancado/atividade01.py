import requests
from bs4 import BeautifulSoup

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