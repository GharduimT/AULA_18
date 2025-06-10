# '''EXEMPLO

# O delegado da delegacia de roubos e furtos de automóveis, entrou em contato solicitando a sua ajuda. Ele lhe pediu para realizar uma observação mais aprofundada, acerca do total de roubos de veiculos, através das cidades do estado do Rio de Janeiro.

# Ele mencionou, que gostaria de um estudo mais aprofundado, no qual pudesse obter informações acerca de como esses dados estão distribuídos, para identificar os grupos de municípios com menos e aqueles com mais roubos de veículos, além de expor, municípios que possuam roubos muito acima do comportamento dos demais municípios do Estado.'''

# '''
# 1 consulta do isp (por conta da demanda do cliente e falta de clareza da proposta)
# 2 Dicionário (em muitos dos casos não se tem domínio dos termos técnicos a respeito da pip)
# '''
# from utils import limpar_nome_municipio
import pandas as pd
import numpy as np

try:
    print('Obtendo dados...')
    #  latin1, utf-8
    ENDERECO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"
    df_ocorrencia = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    #  print(df_ocorrencia.head)

    # for i in range(2):
    #     df_ocorrencia['munic'] = df_ocorrencia['munic'].apply(limpar_nome_municipio)

    #  delimitando variáveis
    #  eu quero apenas duas variaveis de df_ocorrencia
    df_ocorrencia = df_ocorrencia[['munic', 'roubo_veiculo']]
    #  totalizando
    df_roubo_veiculo = df_ocorrencia.groupby('munic').sum(['roubo_veiculo']).reset_index()  # todas as vezes que aparecer o município além de agrupar irá somar as colunas/// reset.index 
    print(df_roubo_veiculo.to_string())

except Exception as e:
    print(f"Erro de conexão: {e}")
    exit()

    #  iniciando análise
try:
    print("Obtendo info sobre padrão de roubos de veículos...")
    #  arrayperformance
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])
    #  MEDIDA DE TENDENCIA CENTRAL
    #  MEDIA
    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    #  MEDIANA
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    #  DISTANCIA
    distancia = abs((media_roubo_veiculo - mediana_roubo_veiculo)/mediana_roubo_veiculo) #*100
    
    print("\nMEDIDAS DE TENÊNCIA CENTRAL")
    print(30*"=")
    print(f'Média de Roubos {media_roubo_veiculo}')
    print(f'Mediana dos Roubos {mediana_roubo_veiculo}')
    print(f'Distância entre a Média e a Mediana {distancia}')

    #  MEDIDAS DE POSIÇÃO
    #  Quartis
    q1 = np.quantile(array_roubo_veiculo, 0.25, method='weibull')  #  weibull é o mais utilizado
    q2 = np.quantile(array_roubo_veiculo, 0.50, method='weibull')
    q3 = np.quantile(array_roubo_veiculo, 0.75, method='weibull')
    
    print("\nMEDIDAS DE TENÊNCIA CENTRAL")
    print(30*"=")
    print(f"Q1: {q1}")
    print(f"Q2: {q2}")
    print(f"Q3: {q3}")

    # ROUBAM MAIS E ROUBAM MENOS
    # ROUBAM MENOS
    df_roubo_veiculo_menores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < q1]
    #ROUBAM MAIS
    df_roubo_veiculo_maiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > q3]

    print("\nMunicípios com menores números de Roubos")
    print(30*"=")
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))
    
    print("\nMunicípios com maiores números de Roubos")
    print(30*"=")
    print(df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False))

    #  IDENTIFICANDO OUTLIERS
    #  IQR
    iqr = q3 - q1

    limite_superior = q3 + (1.5 * iqr)
    limite_inferior = q1 - (1.5 * iqr)

    print("\nLimites - Medidas de Posição")
    print(30*"=")
    print(f'Limite inferior: {limite_inferior}')
    print(f'Limite superior: {limite_superior}')

    #Descobrindo Outliers
    df_roubo_veiculo_outliers_superiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]
    df_roubo_veiculo_outliers_inferiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]

    print("\nOuliers Inferiores")
    print(45*"=")
    if len(df_roubo_veiculo_outliers_inferiores) == 0:
        print('Não há OUTLIERS inferiores')
    else:
        print(df_roubo_veiculo_outliers_inferiores.sort_values(by='roubo_veiculo', ascending=True))
    
    print("\nOuliers Superiores")
    print(45*"=")
    if len(df_roubo_veiculo_outliers_superiores) == 0:
        print('Não há OUTLIERS superiores')
    else:
        print(df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=False))
         

except Exception as e:
    print(f'Erro no processamento das medidas {e}')