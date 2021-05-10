# Importando as bibliotecas necessárias para o projeto
import pandas as pd


# OBTENDO OS DADOS DO PAINEL 1
# Lendo toda a tabela TP_COMGAP e transformando em DataFrame.
dfTpHist = pd.read_csv('./database/TP COMGAP 2015 a 2021.csv')


# OBTENDO OS DADOS DOS FILTROS
# DropDown OM
# Lendo a coluna UNIDADE e transformando em DataFrame.
dfOrganizacoes = dfTpHist.sort_values('UNIDADE', ascending=True).drop_duplicates('UNIDADE').UNIDADE
# DropDown POSTO
dfPosto = dfTpHist.sort_values('POSTO', ascending=True).drop_duplicates('POSTO').POSTO
# DropDown QUADRO
dfQuadro = dfTpHist.sort_values('QUADRO', ascending=True).drop_duplicates('QUADRO').QUADRO
# DropDown ESPECIALIDADE
dfEsp = dfTpHist.sort_values('ESPEC', ascending=True).drop_duplicates('ESPEC').ESPEC
# DropDown AREAS
dfAreas = dfTpHist.sort_values('COMANDO', ascending=True).drop_duplicates('COMANDO').COMANDO
# DropDown ODGSA
dfODGSA = dfTpHist.sort_values('ODGSA', ascending=True).drop_duplicates('ODGSA').ODGSA
# DropDown ANO
dfAno = dfTpHist.sort_values('ANO', ascending=False).drop_duplicates('ANO').ANO
