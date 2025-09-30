import requests
import time
import pandas as pd

url = 'https://rickandmortyapi.com/api/character/'
while True:
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        dados = response.json()
        print(dados['info']['next'])
        break
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            print('limite de requisição excedido, aguarde 10 segundos')
            time.sleep(10)
            continue
        else:
            print(f'Erro inesperado: {e}')
            break


