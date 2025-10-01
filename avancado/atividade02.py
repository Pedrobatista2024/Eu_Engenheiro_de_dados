#Tarefa:
#
#Escolha uma API com Limites: Identifique e utilize uma API que tenha um limite de requisições por segundo ou por minuto. Uma boa opção seria a API do Twitter (agora X) ou, se preferir uma opção mais simples, a API do Trefle.io (para dados botânicos) que tem um limite generoso mas simula o cenário. Para o propósito da nossa simulação, você pode escolher qualquer uma.
#
#Lidar com Rate Limiting: Simule um cenário em que você excede o limite de requisições. Para isso, você pode fazer múltiplas requisições sequenciais e, quando a API retornar um erro de "rate limit exceeded" (geralmente status code 429), implemente uma lógica de espera.
#
#A lógica deve ser: se a requisição falhar por excesso de limite, pause a execução do código por alguns segundos (time.sleep()) e tente novamente.
#
#Coleta de Dados Paginados: Se a API que você escolher retornar dados em várias páginas, implemente a lógica para percorrer todas as páginas e coletar todos os dados disponíveis. Isso é comum em APIs com grandes volumes de dados.

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
        #for p in range(len(dados['results'])):
        #    todos_os_dados.append(dados['results'][p]['name'])
        todos_os_dados.extend(dados['results'])

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

df = pd.DataFrame(todos_os_dados)
print("\ncoleta detodos os personagens finalizada")
print(df.head())


