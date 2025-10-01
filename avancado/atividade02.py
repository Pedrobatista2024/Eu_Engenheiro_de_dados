import requests
import time
import pandas as pd

url = 'https://rickandmortyapi.com/api/character/'
todos_os_dados = []
while url:
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        dados = response.json()
        for p in range(len(dados['results'])):
            todos_os_dados.append 
            (dados['results'][p]['name'])

        url = dados['info']['next']
        
        print(f"Página coletada. Próxima URL: {url}")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            print('limite de requisição excedido, aguarde 10 segundos')
            time.sleep(10)
            continue
        else:
            print(f'Erro inesperado: {e}')
            break

print(todos_os_dados)


