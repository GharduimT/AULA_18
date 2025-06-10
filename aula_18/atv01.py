# ATIVIDADE

# O delegado da delegacia de roubos e furtos de automóveis, entrou em contato pedindo-The ajuda, para realizar uma observação, mais aprofundada acerca do total de casos de estelionatos, através das cidades do estado do Rio de Janeiro.

# Ele mencionou, que gostaria de obter Informações acerca de como estes dados estão distribuídos, se há ou não um padrão destes casos de estelionatos, através das cidades, bem como identificar os municipios com menos casos e aqueles com mais casos de estelionatos e se há alguma cidade, que apresenta uma quantidade discrepante em relação as outras.

import pandas as pd
import numpy as np

try:
    print('Localizando informações...')
    ENDERECO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"
    df_esteilionatos = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')

    # for i in range(2):
    #     df_esteilionatos['munic'] = df_esteilionatos['munic']
    
    df_esteilionatos = df_esteilionatos[['munic', 'roubo_veiculo']]

    df_roubo_veiculo = df_esteilionatos.groupby('munic').sum(['roubo_veiculo']).reset_index()
    print(df_esteilionatos.to_string())

except Exception as e:
    print(f"Erro de conexão: {e}")
    exit()

