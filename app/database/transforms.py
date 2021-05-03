# Importando as bibliotecas necessárias para o projeto
import pandas as pd

from database import connection

# variáveis globais

# criando conexão com banco de dados
cnx = connection.conectar_com_banco('producao')

# OBTENDO OS DADOS DO PAINEL 1
# Lendo toda a tabela view_tp_sisceab_atual e transformando em DataFrame.
dfTpAtual = pd.read_sql_table('view_tp_sisceab_atual', cnx)
# Lendo toda a tabela view_tp_sisceab e transformando em DataFrame.
dfTpHist = pd.read_sql_table('view_tp_sisceab', cnx)

dictUnidadeComando = dfTpAtual[['UNIDADE', 'COMANDO']].sort_values('UNIDADE', ascending=True)\
    .drop_duplicates('UNIDADE').set_index('UNIDADE').T.to_dict('list')

# preencher COMANDO na TP HIST
for index, i in dfTpHist.iterrows():
    unidade = dfTpHist.loc[index, 'UNIDADE']
    comando = dictUnidadeComando.get(unidade, [unidade])
    if comando is not None and comando != '' and comando != []:
        dfTpHist.loc[index, 'COMANDO'] = comando[0]
    else:
        dfTpHist.loc[index, 'COMANDO'] = unidade

# OBTENDO OS DADOS DO PAINEL 2
# Lendo toda a tabela view_solicitamovi e transformando em DataFrame.
dfSolicitaMov = pd.read_sql_table('view_solicitamovi', cnx)
# Lendo toda a tabela view_entrada_saida e transformando em DataFrame.
dfEntradaSaida = pd.read_sql_table('view_entrada_saida', cnx)

# OBTENDO OS DADOS DOS FILTROS
# DropDown OM
# Lendo toda a tabela view_organizacoes_decea e transformando em DataFrame.
dfOrganizacoes = pd.read_sql_table('view_organizacoes_decea', cnx,
                                   columns=['UNIDADE', 'Codigo_Unidade', 'COMANDO', 'Codigo_Comando'])
# DropDown POSTO
dfPosto = pd.read_sql_table('petp', cnx)
# DropDown QUADRO
dfQuadro = pd.read_sql_table('petq', cnx)
# DropDown ESPECIALIDADE
dfEsp = pd.read_sql_table('petesp', cnx)
# DropDown AREAS
dfAreas = dfTpAtual.sort_values('COMANDO', ascending=True).drop_duplicates('COMANDO').COMANDO
