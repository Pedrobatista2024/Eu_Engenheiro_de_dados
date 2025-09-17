#Atividade 6/9: Transformação de Dados e Análise de Janela Móvel
#Nossos analistas precisam de uma visão mais detalhada sobre a performance recente do Bitcoin. Eles solicitaram que você realize uma análise de janela móvel para suavizar as flutuações diárias e identificar tendências de longo prazo.
#
#Tarefa:
#
#Carregar Dados: Use o arquivo Parquet que você criou na tarefa anterior. Garanta que o DataFrame esteja ordenado pela coluna de data.
#
#Transformação: Adicione uma nova coluna ao DataFrame chamada media_movel_7d.
#
#Esta coluna deve conter a média móvel do preço do Bitcoin nos últimos 7 dias. Use a função de janela móvel do Pandas para isso.
#
#Análise Final: Com a nova coluna adicionada, responda às seguintes perguntas:
#
#Em qual data a média móvel de 7 dias cruzou o preço real do Bitcoin de baixo para cima? (Isso pode indicar um sinal de alta)
#
#Em qual data a média móvel de 7 dias cruzou o preço real do Bitcoin de cima para baixo? (Isso pode indicar um sinal de baixa)

import pandas as pd

pd.set_option('display.max_rows', None)

df = pd.read_parquet('dados_combinados.parquet')

df.sort_values(by='data', inplace=True)

df['media_movel_7d'] = df['preco'].rolling(window=7).mean()

df['boleana'] = df['preco'] > df['media_movel_7d']

print(df.head(69))
