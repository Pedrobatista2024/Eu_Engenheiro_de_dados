#Tarefa:
#
#Escolha de Destino: Simule o carregamento dos dados em um banco de dados SQLite (um banco de dados em arquivo que pode ser usado localmente sem um servidor). Você pode usar a biblioteca sqlite3 do Python ou o SQLAlchemy.
#
#Desaninhamento (Flattening): Os dados do Rick and Morty são aninhados. Por exemplo, informações de origin e location são objetos JSON com name e url. Para armazenar isso em uma tabela relacional, você deve desaninhar os dados.
#
#Crie uma coluna para o Nome da Origem e outra para o Nome da Localização (ignorando as URLs).
#
#Modelagem (Criação de Tabelas): Modele os dados em duas tabelas separadas para simular um schema relacional simples:
#
#Tabela 1: personagens (ID, Nome, Status, Espécie, Gênero, ID_Localizacao, ID_Origem)
#
#Tabela 2: localizacoes (ID_Localizacao, Nome_Localizacao).
#
#Nota: Não é necessário criar chaves estrangeiras reais, basta criar um identificador único para as localizações e origens no DataFrame e usá-lo nas duas tabelas.
#
#Carregamento (Loading): Salve os dois DataFrames resultantes em duas tabelas separadas no seu arquivo SQLite.
#
#Para a entrega, envie o código que realiza a modelagem, o desaninhamento e o carregamento no banco de dados SQLite. Me diga o nome do arquivo SQLite que você criou.

import requests
import time
import pandas as pd

pd.set_option('display.max_columns', None)

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


df['nome_origem'] = df['origin'].apply(lambda x: x['name'])

df['nome_localizacao'] = df['location'].apply(lambda x: x['name'])

df.rename(columns={'id': 'id_personagem'}, inplace=True)

df.drop(columns=['origin', 'location'], inplace=True)

print(df.head())

localizacoes = pd.concat([df['nome_localizacao'], df['nome_origem']]).unique()

df_localizacoes = pd.DataFrame(localizacoes, columns=['nome_localizacao'])

df_localizacoes.reset_index(inplace=True)
df_localizacoes.rename(columns={'index': 'id_localizacao'}, inplace=True)

print(df_localizacoes.head())

df = pd.merge(
    df, 
    df_localizacoes,
    left_on='nome_localizacao', 
    right_on='nome_localizacao',
    how='left'
)

df.rename(columns={'id_localizacao': 'id_localizacao_fk'}, inplace=True)
df.drop(columns=['nome_localizacao'], inplace=True)


df = pd.merge(
    df,
    df_localizacoes,
    left_on='nome_origem', 
    right_on='nome_localizacao',
    how='left',
    suffixes=('_pers', '_orig') 
)
df.rename(columns={'id_localizacao': 'id_origem_fk'}, inplace=True)
df.drop(columns=['nome_origem', 'nome_localizacao'], inplace=True) 

colunas_personagens = [
    'id_personagem', 'name', 'status', 'species', 'gender', 
    'id_localizacao_fk', 'id_origem_fk'
]
df_personagens_final = df[colunas_personagens]


df_personagens_final.rename(columns={
    'name': 'nome', 'status': 'status', 'species': 'espécie', 'gender': 'gênero'
}, inplace=True)

print(df_personagens_final.head())