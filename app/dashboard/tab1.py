# Importando as bibliotecas necessárias para o projeto
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output

from app import dash_app
from database import transforms

import pandas as pd
from math import ceil

# variáveis para construção do PAINEL 1
dfOrganizacoesDropDown = transforms.dfOrganizacoes.tolist()
dfPostosDropDown = transforms.dfPosto.tolist()
dfQuadrosDropDown = transforms.dfQuadro.tolist()
dfEspecialidadeDropDown = transforms.dfEsp.tolist()
dfAreasDropDown = transforms.dfAreas.tolist()
dfAnosDropDown = transforms.dfAno.tolist()

# variaveis de dados construção do PAINEL 1
dfTpHist = transforms.dfTpHist
dfTpHist = dfTpHist.fillna("-")  # Substituindo registro nulos por "-"
dfTpHist.replace('', '-', inplace=True)  # Substituindo registro vazio por "-"

ano_atual = int(dfAnosDropDown[0])
ano_anterior = ano_atual - 1

# variáveis para construção da TABELA do PAINEL 1
dfColumnsTable = ['indice', 'UNIDADE', 'POSTO', 'QUADRO', 'ESPEC', 'PROPOSTO', 'TP_ANO_ATUAL', 'EXISTENTE', 'EXI_PTTC', 'Dif(EXI)', 'Dif(EXI+PTTC)', 'STATUS']
PAGE_SIZE = 100

# MONTANDO ESTRUTURA DO DASHBOARD DO PAINEL 1
tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.Div(  # PAINEL
                [
                    dbc.Row(  # FILTRO, CARD TOTAL INDICADORES E GRAFICO PRINCIPAL
                        [
                            dbc.Col(  # FILTRO e CARD TOTAL
                                [
                                    dbc.Card([  # FILTROS DE PESQUISA
                                        dbc.CardBody([
                                            html.H4(children='Filtros:', style={'textAlign': 'left'}),
                                            html.Div([
                                                html.Label(children='Áreas (Regionais):',
                                                           style={'text-align': 'left', 'font-weight': 'bold'}),
                                                html.Div([
                                                    dcc.Dropdown(
                                                        id='input-area',
                                                        options=[{'label': sigla, 'value': sigla} for sigla
                                                                 in dfAreasDropDown],
                                                        value='',
                                                        multi=True,
                                                        placeholder="Filtrar por Área"
                                                    )
                                                ]),
                                                html.Label(children='Organização:',
                                                           style={'text-align': 'left', 'font-weight': 'bold'}),
                                                html.Div([
                                                    dcc.Dropdown(
                                                        id='input-om',
                                                        options=[{'label': sigla, 'value': sigla} for sigla
                                                                 in dfOrganizacoesDropDown],
                                                        value='',
                                                        multi=True,
                                                        placeholder="Filtrar por OM"
                                                    )
                                                ]),
                                                html.Label(children='Posto/Graduação:',
                                                           style={'text-align': 'left', 'font-weight': 'bold'}),
                                                html.Div([
                                                    dcc.Dropdown(
                                                        id='input-posto',
                                                        options=[{'label': posto, 'value': posto} for posto
                                                                 in dfPostosDropDown],
                                                        value='',
                                                        multi=True,
                                                        placeholder="Filtrar por Posto/Graduação"
                                                    )
                                                ]),
                                                html.Label(children='Quadro:',
                                                           style={'text-align': 'left', 'font-weight': 'bold'}),
                                                html.Div([
                                                    dcc.Dropdown(
                                                        id='input-quadro',
                                                        options=[{'label': quadro, 'value': quadro} for quadro
                                                                 in dfQuadrosDropDown],
                                                        value='',
                                                        multi=True,
                                                        placeholder="Filtrar por Quadro"
                                                    )
                                                ]),
                                                html.Label(children='Especialidade:',
                                                           style={'text-align': 'left', 'font-weight': 'bold'}),
                                                html.Div([
                                                    dcc.Dropdown(
                                                        id='input-especialidade',
                                                        options=[{'label': especialidade, 'value': especialidade}
                                                                 for especialidade in dfEspecialidadeDropDown],
                                                        value='',
                                                        multi=True,
                                                        placeholder="Filtrar por Especialidade"
                                                    )
                                                ]),
                                            ], style={})
                                        ])
                                    ], color="light"),
                                ],
                                width=2
                            ),
                            dbc.Col(  # GRAFICO PRINCIPAL INDICADORES
                                dcc.Graph(id='graph-1', config={'displayModeBar': False}),
                                width=2
                            ),
                            dbc.Col(  # INDICADOR PRINCIPAL
                                dcc.Graph(id='indicador-1', config={'displayModeBar': False}),
                                width=3
                            ),
                            dbc.Col(  # GRAFICO HISTORICO
                                dcc.Graph(id='graph-2', config={'displayModeBar': False}),
                                width=5
                            ),
                        ]
                    ),
                    dbc.Row(  # GRAFICOS DA TAXA OCUPAÇÃO POR ÁREA
                        [
                            dbc.Col(  # BARRAS TAXA OCUPAÇÃO POR ÁREA
                                dcc.Graph(id='graph-taxa-area', config={'displayModeBar': False}),
                                width=12,
                            ),
                        ],
                        no_gutters=True
                    ),
                    dbc.Row(  # GRAFICOS DA TP
                        [
                            dbc.Col(  # BARRAS TP POR OM
                                dcc.Graph(id='graph-tp-om', config={'displayModeBar': False}),
                                width=6,
                            ),
                            dbc.Col(  # BARRAS DIFERENÇA TP POR OM
                                dcc.Graph(id='graph-tp-dif-om', config={'displayModeBar': False}),
                                width=6,
                            ),
                        ],
                        no_gutters=True
                    ),
                    dbc.Row(  # PIZZAS TABELA DE PESSOAL
                        [
                            dbc.Col([  # PIZZAS
                                html.H5(children=f'Percentuais da TP em {ano_atual}:',
                                        style={'text-align': 'left', 'vertical-align': 'super'}),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Graph(id='graph-pie-tp-area',
                                                      config={'staticPlot': True, 'displayModeBar': False})),
                                        dbc.Col(
                                            dcc.Graph(id='graph-pie-tp-om',
                                                      config={'staticPlot': True, 'displayModeBar': False})),
                                        dbc.Col(
                                            dcc.Graph(id='graph-pie-tp-posto',
                                                      config={'staticPlot': True, 'displayModeBar': False})),
                                        dbc.Col(
                                            dcc.Graph(id='graph-pie-tp-quadro',
                                                      config={'staticPlot': True, 'displayModeBar': False})),
                                        dbc.Col(
                                            dcc.Graph(id='graph-pie-tp-especialidade',
                                                      config={'staticPlot': True, 'displayModeBar': False})),
                                    ],
                                    no_gutters=True,
                                )], width=12
                            ),
                        ],
                        no_gutters=True
                    ),
                    dbc.Row(  # TABELA DE PESSOAL
                        [
                            dbc.Col(  # TABELA
                                html.Div([
                                    html.H5(children=f'Tabela de Pessoal {ano_atual}:',
                                            style={'text-align': 'left', 'vertical-align': 'super',
                                                   'margin': '5px', 'margin-bottom': '10px'}),
                                    html.Div([
                                        dash_table.DataTable(
                                            id='datatable-paging',
                                            columns=[
                                                {'name': i, 'id': i, 'deletable': True} for i in dfColumnsTable
                                            ],
                                            fixed_rows={'headers': True},
                                            style_table={'height': '500px', 'overflowY': 'auto'},
                                            style_as_list_view=True,
                                            style_header={
                                                'backgroundColor': 'rgb(230, 230, 230)',
                                                'fontWeight': 'bold',
                                                'textAlign': 'center'
                                            },
                                            style_cell={
                                                'minWidth': 75, 'maxWidth': 95, 'textAlign': 'center'
                                            },
                                            style_cell_conditional=[
                                                {
                                                    'if': {'column_id': c},
                                                    'textAlign': 'left'
                                                } for c in ['UNIDADE', 'POSTO', 'QUADRO', 'ESPEC']
                                            ],
                                            style_data_conditional=[
                                                {
                                                    'if': {'row_index': 'odd'},
                                                    'backgroundColor': 'rgb(248, 248, 248)'
                                                },
                                                {
                                                    'if': {
                                                        'column_id': ['indice', 'STATUS', 'PROPOSTO', 'TP_ANO_ATUAL',
                                                                      'EXISTENTE', 'EXI_PTTC',
                                                                      'Dif(EXI)', 'Dif(EXI+PTTC)'],
                                                    },
                                                    'textAlign': 'center',
                                                    'width': 95
                                                },
                                                {
                                                    'if': {
                                                        'filter_query': '{Dif(EXI)} < 0 && {Dif(EXI+PTTC)} < 0'
                                                    },
                                                    'color': 'white',
                                                    'backgroundColor': 'rgb(250, 128, 114)'
                                                },
                                                {
                                                    'if': {
                                                        'column_id': 'Dif(EXI)',
                                                        'filter_query': '{Dif(EXI)} < 0'
                                                    },
                                                    'color': 'red',
                                                    'fontWeight': 'bold',
                                                },
                                                {
                                                    'if': {
                                                        'column_id': 'Dif(EXI+PTTC)',
                                                        'filter_query': '{Dif(EXI+PTTC)} < 0'
                                                    },
                                                    'color': 'red',
                                                    'fontWeight': 'bold',
                                                },
                                            ],
                                            page_current=0,
                                            page_size=PAGE_SIZE,
                                            page_action='custom',

                                            filter_action='custom',
                                            filter_query='',

                                            sort_action='custom',
                                            sort_mode='multi',
                                            sort_by=[],
                                        )
                                    ]),
                                ], style={'margin-top': '0px'}),
                                width=12
                            ),
                        ],
                        no_gutters=True
                    ),
                ]
            ),
        ]
    ),
    className="mt-3",
)


@dash_app.callback(
    [Output('graph-1', 'figure'),
     Output('indicador-1', 'figure'),
     Output('graph-2', 'figure'),
     Output('graph-tp-om', 'figure'),
     Output('graph-pie-tp-om', 'figure'),
     Output('graph-tp-dif-om', 'figure'),
     Output('graph-pie-tp-area', 'figure'),
     Output('graph-pie-tp-posto', 'figure'),
     Output('graph-pie-tp-quadro', 'figure'),
     Output('graph-pie-tp-especialidade', 'figure'),
     Output('graph-taxa-area', 'figure'),
     ],
    [Input('input-area', 'value'),
     Input('input-om', 'value'),
     Input('input-posto', 'value'),
     Input('input-quadro', 'value'),
     Input('input-especialidade', 'value'),
     ])
def update_data_painel_1(input_area_value, input_om_value,
                         input_posto_value, input_quadro_value, input_especialidade_value):
    dfTpAtual = dfTpHist[dfTpHist['ANO'] == ano_atual]
    filtered_df_tp_atual = dfTpHist[dfTpHist['ANO'] == ano_atual]
    filtered_df_tp_hist = dfTpHist[dfTpHist['ANO'] != ano_atual]

    x_label = [f'COMGAP {ano_atual}']
    # filtrando DF pela AREA
    if input_area_value is not None and input_area_value != '' and input_area_value != []:
        filtered_df_tp_atual = filtered_df_tp_atual.loc[filtered_df_tp_atual['COMANDO'].isin(input_area_value)]
        filtered_df_tp_hist = filtered_df_tp_hist.loc[filtered_df_tp_hist['COMANDO'].isin(input_area_value)]
        x_label = ['OM Filtrada(s)']
    # filtrando DF pela OM
    if input_om_value is not None and input_om_value != '' and input_om_value != []:
        filtered_df_tp_atual = filtered_df_tp_atual.loc[filtered_df_tp_atual['UNIDADE'].isin(input_om_value)]
        filtered_df_tp_hist = filtered_df_tp_hist.loc[filtered_df_tp_hist['UNIDADE'].isin(input_om_value)]
        x_label = [', '.join(input_om_value)]
    # filtrando DF pela POSTO
    if input_posto_value is not None and input_posto_value != '' and input_posto_value != []:
        filtered_df_tp_atual = filtered_df_tp_atual.loc[filtered_df_tp_atual['POSTO'].isin(input_posto_value)]
        filtered_df_tp_hist = filtered_df_tp_hist.loc[filtered_df_tp_hist['POSTO'].isin(input_posto_value)]
    # filtrando DF pela QUADRO
    if input_quadro_value is not None and input_quadro_value != '' and input_quadro_value != []:
        filtered_df_tp_atual = filtered_df_tp_atual.loc[filtered_df_tp_atual['QUADRO'].isin(input_quadro_value)]
        filtered_df_tp_hist = filtered_df_tp_hist.loc[filtered_df_tp_hist['QUADRO'].isin(input_quadro_value)]
    # filtrando DF pela ESPEC
    if input_especialidade_value is not None and input_especialidade_value != '' and input_especialidade_value != []:
        filtered_df_tp_atual = filtered_df_tp_atual.loc[filtered_df_tp_atual['ESPEC'].isin(input_especialidade_value)]
        filtered_df_tp_hist = filtered_df_tp_hist.loc[filtered_df_tp_hist['ESPEC'].isin(input_especialidade_value)]

    # MONTANDO DADOS DOS GRAFICOS 1, 2 e 3
    # calcular totalizadores da TP ATUAL (SEM FILTRO)
    total_tp_atual_sem_filtro = int(sum(dfTpAtual['TP_ANO_ATUAL']))
    total_existe_ativo_sem_filtro = int(sum(dfTpAtual['EXISTENTE']))
    # calcular indices da TP ATUAL
    if total_tp_atual_sem_filtro > 0:
        indice_efetivo_ativo_sem_filtro = (total_existe_ativo_sem_filtro / total_tp_atual_sem_filtro) * 100
    else:  # TP inexistente
        indice_efetivo_ativo_sem_filtro = 0
    # calcular totalizadores da TP ATUAL
    total_proposto = int(sum(filtered_df_tp_atual['PROPOSTO']))
    total_tp_atual = int(sum(filtered_df_tp_atual['TP_ANO_ATUAL']))
    total_existe_ativo = int(sum(filtered_df_tp_atual['EXISTENTE']))
    total_existe_ttc = int(sum(filtered_df_tp_atual['EXI_PTTC']))
    total_existe_civil = int(sum(filtered_df_tp_atual['EXISTCIVIL']))
    total_efetivo_ativo_ttc = int(total_existe_ativo + total_existe_ttc)
    total_efetivo_ativo_ttc_cv = int(total_existe_ativo + total_existe_ttc + total_existe_civil)
    # calcular indices da TP ATUAL
    if total_tp_atual > 0:
        indice_efetivo_ativo = (total_existe_ativo / total_tp_atual) * 100
        indice_efetivo_ativo_ttc = (total_efetivo_ativo_ttc / total_tp_atual) * 100
        indice_efetivo_ativo_ttc_cv = (total_efetivo_ativo_ttc_cv / total_tp_atual) * 100
    else:  # TP inexistente
        indice_efetivo_ativo = 0
        indice_efetivo_ativo_ttc = 0
        indice_efetivo_ativo_ttc_cv = 0
    # Montar totalizadores HISTORICOS das TP do COMGAP com a TP ATUAL
    df_totais_hist = filtered_df_tp_hist.groupby('ANO', as_index=False).sum()
    df_totais_hist_atual = pd.DataFrame(
        [(ano_atual, total_tp_atual, total_existe_ativo, total_existe_ttc, total_existe_civil, total_proposto)],
        columns=['ANO', 'TP_ANO_ATUAL', 'EXISTENTE', 'EXI_PTTC', 'EXISTCIVIL', 'PROPOSTO'])
    df_totais_hist_atual = df_totais_hist_atual.append(
        df_totais_hist.sort_values(by='ANO', ascending=False), ignore_index=True)
    # calcular indices da TP ANO ANTERIOR
    df_totais_ano_anterior = df_totais_hist_atual[df_totais_hist_atual['ANO'] == ano_anterior]
    total_existe_ativo_ano_anterior = int(df_totais_ano_anterior.EXISTENTE)
    total_tp_atual_ano_anterior = int(df_totais_ano_anterior.TP_ANO_ATUAL)
    total_efetivo_ativo_ttc_ano_anterior = int(df_totais_ano_anterior.EXISTENTE + df_totais_ano_anterior.EXI_PTTC)
    total_efetivo_ativo_ttc_cv_ano_anterior = \
        int(total_efetivo_ativo_ttc_ano_anterior + df_totais_ano_anterior.EXISTCIVIL)
    if total_tp_atual > 0:
        indice_efetivo_ativo_ano_anterior = (total_existe_ativo_ano_anterior / total_tp_atual_ano_anterior) * 100
        indice_efetivo_ativo_ttc_ano_anterior = \
            (total_efetivo_ativo_ttc_ano_anterior / total_tp_atual_ano_anterior) * 100
        indice_efetivo_ativo_ttc_cv_ano_anterior = \
            (total_efetivo_ativo_ttc_cv_ano_anterior / total_tp_atual_ano_anterior) * 100
    else:  # TP inexistente
        indice_efetivo_ativo_ano_anterior = 0
        indice_efetivo_ativo_ttc_ano_anterior = 0
        indice_efetivo_ativo_ttc_cv_ano_anterior = 0
    # Montar totalizadores da TP ATUAL por UNIDADE, AREA, POSTO, QUADRO, ESPC
    df_totais_atual_por_om = filtered_df_tp_atual.groupby('UNIDADE', as_index=False).sum()
    df_totais_atual_por_area = filtered_df_tp_atual.groupby('COMANDO', as_index=False).sum()
    df_totais_atual_por_posto = filtered_df_tp_atual.groupby('POSTO', as_index=False).sum()
    df_totais_atual_por_quadro = filtered_df_tp_atual.groupby('QUADRO', as_index=False).sum()
    df_totais_atual_por_especialidade = filtered_df_tp_atual.groupby('ESPEC', as_index=False).sum()

    # GRAFICO 1 - barras EFETIVO X TP
    trace_bar_proposto = go.Bar(x=x_label, y=[total_proposto], name='TP Proposta',
                                textposition='auto', text=total_proposto, hoverinfo='none',
                                marker={'color': '#00CC96'})
    trace_bar_atual = go.Bar(x=x_label, y=[total_tp_atual], name='TP Atual',
                             textposition='auto', text=total_tp_atual, hoverinfo='none',
                             marker={'color': '#000000'})
    trace_bar_ativo = go.Bar(x=x_label, y=[total_existe_ativo], name='Efetivo Ativo',
                             textposition='auto', text=total_existe_ativo, hoverinfo='none',
                             marker={'color': '#3587FA'})
    trace_bar_ttc = go.Bar(x=x_label, y=[total_existe_ttc], name='Efetivo PTTC',
                           textposition='auto', text=total_existe_ttc, hoverinfo='none',
                           marker={'color': '#808080'})
    trace_bar_cv = go.Bar(x=x_label, y=[total_existe_civil], name='Efetivo Cv',
                          textposition='auto', text=total_existe_civil, hoverinfo='none',
                          marker={'color': '#ff7f0e'})
    trace_bar_forca = go.Bar(x=x_label,
                             y=[(total_existe_ativo + total_existe_ttc + total_existe_civil)],
                             name='Ativo + PTTC + Civil',
                             textposition='auto',
                             text=(total_existe_ativo + total_existe_ttc + total_existe_civil), hoverinfo='none',
                             marker={'color': '#244e76'},
                             visible='legendonly')
    # Armazenando as Barras em uma lista
    data = [trace_bar_proposto, trace_bar_atual, trace_bar_ativo, trace_bar_ttc, trace_bar_cv, trace_bar_forca]
    # Criando Layout
    layout = go.Layout(title=f'Efetivo e TP {ano_atual}',
                       titlefont={'color': '#2fa4e7', 'size': 20},
                       legend_orientation='h',
                       legend_font_size=12)
    # Criando figura que será exibida
    figure1 = go.Figure(data=data, layout=layout)
    figure1.update_layout(transition_duration=500, hovermode='x', margin=dict(r=10, t=35, b=10, l=10))

    # GRAFICO 2 - gauge-charts INDICE TP
    trace_gauge_charts = go.Indicator(
        mode="gauge+number+delta",
        value=indice_efetivo_ativo,
        title={'text': f'<span style="color:#3587FA"><b>Taxa do Efetivo Ativo:</b> '
                       f'{indice_efetivo_ativo:.1f}%</span><br>'
                       f'<span style="color:#808080"><b>Taxa do Efetivo Ativo + PTTC:</b> '
                       f'{indice_efetivo_ativo_ttc:.1f}%</span><br>'
                       f'<span style="color:#244e76"><b>Taxa da Força de Trabalho<br>(Ativo + PTTC + Cv):</b> '
                       f'{indice_efetivo_ativo_ttc_cv:.1f}%</span>',
               'font': {'size': 14}},
        domain={'x': [0, 1], 'y': [0, 1]},
        number={'suffix': "%"},
        delta={'reference': indice_efetivo_ativo_ano_anterior, 'relative': True},
        gauge={
            'shape': "angular",
            'axis': {
                'range': [0, 100],
                'tickwidth': 1,
                'tickcolor': "darkblue",
                'nticks': 10,
                'ticksuffix': "%"
            },
            'bar': {'color': "#3587FA"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "black",
            'steps': [
                {'range': [0, 80], 'color': '#FF261D'},
                {'range': [80, 100], 'color': 'green'}
            ],
            'threshold': {
                'line': {'color': "#244e76", 'width': 6},
                'thickness': 0.85,
                'value': indice_efetivo_ativo_ttc_cv}
        }
    )
    # Armazenando as Barras em uma lista
    data = [trace_gauge_charts]
    # Criando Layout
    layout = go.Layout(title=f'Taxa de Ocupação da TP {ano_atual}',
                       titlefont={'color': '#2fa4e7', 'size': 20})
    # Criando figura que será exibida
    figure2 = go.Figure(data=data, layout=layout)
    figure2.update_layout(margin=dict(r=45, t=35, b=10, l=45))

    # GRAFICO 3 - Scatter TP HISTORICA
    trace_line_proposta = go.Scatter(x=df_totais_hist_atual.ANO, y=df_totais_hist_atual.PROPOSTO,
                                     name='TP Proposta', mode='markers+lines+text', marker={'color': '#00CC96'},
                                     textposition='bottom center', text=df_totais_hist_atual.PROPOSTO, hoverinfo='text',
                                     textfont=dict(color="#00CC96"), visible='legendonly')
    trace_line_tp = go.Scatter(x=df_totais_hist_atual.ANO, y=df_totais_hist_atual.TP_ANO_ATUAL,
                               name='TP', mode='markers+lines+text', marker={'color': '#000000'},
                               textposition='bottom center', text=df_totais_hist_atual.TP_ANO_ATUAL, hoverinfo='text',
                               textfont=dict(color="#000000"))
    trace_line_ativo = go.Scatter(x=df_totais_hist_atual.ANO, y=df_totais_hist_atual.EXISTENTE,
                                  name='Efetivo Ativo', mode='markers+lines+text', marker={'color': '#3587FA'},
                                  textposition='bottom center', text=df_totais_hist_atual.EXISTENTE, hoverinfo='text',
                                  textfont=dict(color="#3587FA"))
    trace_line_ttc = go.Scatter(x=df_totais_hist_atual.ANO, y=df_totais_hist_atual.EXI_PTTC,
                                name='Efetivo PTTC', mode='markers+lines+text', marker={'color': '#808080'},
                                textposition='bottom center', text=df_totais_hist_atual.EXI_PTTC, hoverinfo='text',
                                textfont=dict(color="#808080"))
    trace_line_cv = go.Scatter(x=df_totais_hist_atual.ANO, y=df_totais_hist_atual.EXISTCIVIL,
                               name='Efetivo Civil', mode='markers+lines+text', marker={'color': '#ff7f0e'},
                               textposition='bottom center', text=df_totais_hist_atual.EXISTCIVIL, hoverinfo='text',
                               textfont=dict(color="#ff7f0e"))
    # Criando Layout
    layout_hist_efetivo_tp = go.Layout(title='Evolução histórica do Efetivo e da Tabela de Pessoal',
                                       titlefont={'color': '#2fa4e7', 'size': 20},
                                       legend_orientation='h',
                                       legend_font_size=14)
    # Criando figura que será exibida
    fig_hist_efetivo_tp = make_subplots(rows=2, cols=1)
    fig_hist_efetivo_tp.add_trace(trace_line_proposta, row=1, col=1)
    fig_hist_efetivo_tp.add_trace(trace_line_tp, row=1, col=1)
    fig_hist_efetivo_tp.add_trace(trace_line_ativo, row=1, col=1)

    fig_hist_efetivo_tp.add_trace(trace_line_ttc, row=2, col=1)
    fig_hist_efetivo_tp.add_trace(trace_line_cv, row=2, col=1)

    fig_hist_efetivo_tp.update_layout(layout_hist_efetivo_tp)
    fig_hist_efetivo_tp.update_layout(transition_duration=500, hovermode='x', margin=dict(r=10, t=35, b=10, l=10))

    # GRAFICO 4 - barras TP POR OM
    df_atual_om = df_totais_atual_por_om.sort_values(by='TP_ANO_ATUAL', ascending=False)
    trace_bar_tp_proposto_om = go.Bar(x=df_atual_om.UNIDADE,
                                      y=df_atual_om.PROPOSTO, name='TP Proposta',
                                      marker={'color': '#00CC96'},
                                      visible='legendonly')
    trace_bar_tp_atual_om = go.Bar(x=df_atual_om.UNIDADE,
                                   y=df_atual_om.TP_ANO_ATUAL, name='TP Atual',
                                   marker={'color': '#000000'})
    trace_bar_ativo_om = go.Bar(x=df_atual_om.UNIDADE,
                                y=df_atual_om.EXISTENTE, name='Efetivo Ativo',
                                marker={'color': '#3587FA'})
    trace_bar_tcc_om = go.Bar(x=df_atual_om.UNIDADE,
                              y=df_atual_om.EXI_PTTC, name='Efetivo PTTC',
                              marker={'color': '#808080'},
                              visible='legendonly')
    trace_bar_cv_om = go.Bar(x=df_atual_om.UNIDADE,
                             y=df_atual_om.EXISTCIVIL, name='Efetivo Cv',
                             marker={'color': '#ff7f0e'},
                             visible='legendonly')
    trace_bar_forca_trab = go.Bar(x=df_atual_om.UNIDADE,
                                  y=(df_atual_om.EXISTENTE + df_atual_om.EXI_PTTC + df_atual_om.EXISTCIVIL),
                                  name='Força Trabalho (Ativo + PTTC + Civil)',
                                  marker={'color': '#244e76'},
                                  visible='legendonly')
    # Armazenando as Barras em uma lista
    data_tp_om = [trace_bar_tp_proposto_om, trace_bar_tp_atual_om, trace_bar_ativo_om, trace_bar_forca_trab,
                  trace_bar_tcc_om, trace_bar_cv_om]
    # Criando Layout
    layout_tp_om = go.Layout(title=f'Efetivo e TP {ano_atual} por OM',
                             titlefont={'color': '#2fa4e7', 'size': 20})
    # Criando figura que será exibida
    figure_tp_om = go.Figure(data=data_tp_om, layout=layout_tp_om)
    figure_tp_om.update_layout(transition_duration=500, hovermode='x', margin=dict(r=10, t=35, b=10, l=10),
                               legend=dict(orientation="h", yanchor="top", y=0.99, xanchor="right", x=0.99))

    # GRAFICO 5 - pizza TP POR OM
    trace_pie_tp_om = go.Pie(labels=df_totais_atual_por_om.UNIDADE,
                             values=df_totais_atual_por_om.TP_ANO_ATUAL,
                             marker={'line': {'color': '#000000', 'width': 1}},
                             hoverinfo='label+percent+value',
                             direction='clockwise',
                             textposition='inside',
                             textinfo='percent',
                             hole=.3)
    # Armazenando gráfico em uma lista:
    data_pie_to_om = [trace_pie_tp_om]
    # Criando Layout:
    layout_pie_tp_om = go.Layout(title=f'Por OM', uniformtext_minsize=12, uniformtext_mode='hide')
    # Criando figura que será exibida:
    figure_pie_tp_om = go.Figure(data=data_pie_to_om, layout=layout_pie_tp_om)
    figure_pie_tp_om.update_layout(margin=dict(r=10, t=35, b=10, l=10))

    # GRAFICO 6 - barras TP DIFERENÇA POR OM
    trace_bar_dif_ativo_om = go.Bar(x=df_atual_om.UNIDADE,
                                    y=df_atual_om['Dif(EXI)'], name='Efetivo Ativo',
                                    marker={'color': '#3587FA'})
    trace_bar_dif_ativo_tcc_cv_om = go.Bar(x=df_atual_om.UNIDADE,
                                           y=((df_atual_om.EXISTENTE + df_atual_om.EXI_PTTC + df_atual_om.EXISTCIVIL) - df_atual_om.TP_ANO_ATUAL),
                                           name='Força Trabalho (Ativo + PTTC + Civil)',
                                           marker={'color': '#244e76'}, visible='legendonly')
    # Armazenando as Barras em uma lista
    data_dif_om = [trace_bar_dif_ativo_om, trace_bar_dif_ativo_tcc_cv_om]
    # Criando Layout
    layout_dif_om = go.Layout(title=f'GAP do Efetivo em relação à TP {ano_atual} por OM',
                              titlefont={'color': '#2fa4e7', 'size': 20},)
    # Criando figura que será exibida
    figure_dif_om = go.Figure(data=data_dif_om, layout=layout_dif_om)
    figure_dif_om.update_layout(transition_duration=500, hovermode='x', margin=dict(r=10, t=35, b=10, l=10),
                                legend=dict(orientation="h", yanchor="top", y=0.99, xanchor="right", x=0.99))

    # GRAFICO 6 - pizza TP POR AREA
    trace_pie_tp_area = go.Pie(labels=df_totais_atual_por_area.COMANDO,
                               values=df_totais_atual_por_area.TP_ANO_ATUAL,
                               marker={'line': {'color': '#000000', 'width': 1}},
                               hoverinfo='label+percent+value',
                               direction='clockwise',
                               textposition='inside',
                               textinfo='percent',
                               hole=.3)
    # Armazenando gráfico em uma lista:
    data_pie_to_area = [trace_pie_tp_area]
    # Criando Layout:
    layout_pie_tp_area = go.Layout(title=f'Por ÁREA', uniformtext_minsize=12, uniformtext_mode='hide')
    # Criando figura que será exibida:
    figure_pie_tp_area = go.Figure(data=data_pie_to_area, layout=layout_pie_tp_area)
    figure_pie_tp_area.update_layout(margin=dict(r=10, t=35, b=10, l=10))

    # GRAFICO 7 - pizza TP POR POSTO
    trace_pie_tp_posto = go.Pie(labels=df_totais_atual_por_posto.POSTO,
                                values=df_totais_atual_por_posto.TP_ANO_ATUAL,
                                marker={'line': {'color': '#000000', 'width': 1}},
                                hoverinfo='label+percent+value',
                                direction='clockwise',
                                textposition='inside',
                                textinfo='percent',
                                hole=.3)
    # Armazenando gráfico em uma lista:
    data_pie_to_posto = [trace_pie_tp_posto]
    # Criando Layout:
    layout_pie_tp_posto = go.Layout(title=f'Por POSTO', uniformtext_minsize=12, uniformtext_mode='hide')
    # Criando figura que será exibida:
    figure_pie_tp_posto = go.Figure(data=data_pie_to_posto, layout=layout_pie_tp_posto)
    figure_pie_tp_posto.update_layout(margin=dict(r=10, t=35, b=10, l=10))

    # GRAFICO 8 - pizza TP POR QUADRO
    trace_pie_tp_quadro = go.Pie(labels=df_totais_atual_por_quadro.QUADRO,
                                 values=df_totais_atual_por_quadro.TP_ANO_ATUAL,
                                 marker={'line': {'color': '#000000', 'width': 1}},
                                 hoverinfo='label+percent+value',
                                 direction='clockwise',
                                 textposition='inside',
                                 textinfo='percent',
                                 hole=.3)
    # Armazenando gráfico em uma lista:
    data_pie_to_quadro = [trace_pie_tp_quadro]
    # Criando Layout:
    layout_pie_tp_quadro = go.Layout(title=f'Por QUADRO', uniformtext_minsize=12, uniformtext_mode='hide')
    # Criando figura que será exibida:
    figure_pie_tp_quadro = go.Figure(data=data_pie_to_quadro, layout=layout_pie_tp_quadro)
    figure_pie_tp_quadro.update_layout(margin=dict(r=10, t=35, b=10, l=10))

    # GRAFICO 9 - pizza TP POR ESPEC
    trace_pie_tp_especialidade = go.Pie(labels=df_totais_atual_por_especialidade.ESPEC,
                                        values=df_totais_atual_por_especialidade.TP_ANO_ATUAL,
                                        marker={'line': {'color': '#000000', 'width': 1}},
                                        hoverinfo='label+percent+value',
                                        direction='clockwise',
                                        textposition='inside',
                                        textinfo='percent',
                                        hole=.3)
    # Armazenando gráfico em uma lista:
    data_pie_to_especialidade = [trace_pie_tp_especialidade]
    # Criando Layout:
    layout_pie_tp_especialidade = go.Layout(title=f'Por ESPECIALIDADE', uniformtext_minsize=12, uniformtext_mode='hide')
    # Criando figura que será exibida:
    figure_pie_tp_especialidade = go.Figure(data=data_pie_to_especialidade, layout=layout_pie_tp_especialidade)
    figure_pie_tp_especialidade.update_layout(margin=dict(r=10, t=35, b=10, l=10))

    # GRAFICO - barras Taxa de Ocupação POR ÁREA
    df_atual_area = df_totais_atual_por_area
    df_atual_area['META'] = indice_efetivo_ativo_sem_filtro
    label_meta = f'Meta em {indice_efetivo_ativo_sem_filtro:.1f}% - Taxa de Ocupação COMGAP {ano_atual}'
    trace_line_meta = go.Scatter(x=df_atual_area.COMANDO,
                                 y=df_atual_area.META, name='Meta Taxa de Ocupação',
                                 mode='markers+lines', marker={'color': '#FF0000', 'size': 4},
                                 line={'color': '#FF0000', 'width': 4},
                                 text=label_meta,
                                 hoverinfo='text')
    trace_bar_taxa_ativo_area = go.Bar(x=df_atual_area.COMANDO,
                                       y=round(
                                           ((df_atual_area.EXISTENTE / df_atual_area.TP_ANO_ATUAL) * 100), 1
                                       ),
                                       name='Taxa Efetivo Ativo',
                                       textposition='outside', texttemplate='%{y}%',
                                       text=round(
                                           ((df_atual_area.EXISTENTE / df_atual_area.TP_ANO_ATUAL) * 100), 1
                                       ),
                                       marker={'color': '#3587FA'}, hoverinfo='text')
    trace_line_taxa_forca_trab = go.Bar(x=df_atual_area.COMANDO,
                                        y=round(
                                            (((df_atual_area.EXISTENTE + df_atual_area.EXI_PTTC + df_atual_area.EXISTCIVIL) /
                                            df_atual_area.TP_ANO_ATUAL) * 100),
                                            1
                                        ),
                                        name='Taxa Força Trabalho (Ativo + PTTC + Civil)',
                                        textposition='outside', texttemplate='%{y}%',
                                        text=round(
                                            (((df_atual_area.EXISTENTE + df_atual_area.EXI_PTTC + df_atual_area.EXISTCIVIL) /
                                            df_atual_area.TP_ANO_ATUAL) * 100), 1
                                        ),
                                        marker={'color': '#244e76'}, hoverinfo='text', visible='legendonly')
    # Armazenando as Barras em uma lista
    data_taxa_area = [trace_bar_taxa_ativo_area, trace_line_taxa_forca_trab, trace_line_meta]
    # Criando Layout
    layout_taxa_area = go.Layout(title=f'Taxa de Ocupação da TP {ano_atual} por Área (regional)',
                                 titlefont={'color': '#2fa4e7', 'size': 20})
    # Criando figura que será exibida
    figure_taxa_area = go.Figure(data=data_taxa_area, layout=layout_taxa_area)
    figure_taxa_area.update_layout(transition_duration=500, hovermode='x', margin=dict(r=10, t=35, b=10, l=10),
                                   legend=dict(orientation="h", yanchor="top", y=0.99, xanchor="right", x=0.99))


    return figure1, figure2, fig_hist_efetivo_tp, figure_tp_om, figure_pie_tp_om, \
           figure_dif_om, figure_pie_tp_area, figure_pie_tp_posto, figure_pie_tp_quadro, figure_pie_tp_especialidade, \
           figure_taxa_area


# variáveis para construção da tabela do PAINEL 1
operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if v0 == value_part[-1] and v0 in ("'", '"', '`'):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3


@dash_app.callback(
    Output('datatable-paging', 'data'),
    Output('datatable-paging', 'page_count'),
    Input('input-area', 'value'),
    Input('input-om', 'value'),
    Input('input-posto', 'value'),
    Input('input-quadro', 'value'),
    Input('input-especialidade', 'value'),
    Input('datatable-paging', "page_current"),
    Input('datatable-paging', "page_size"),
    Input('datatable-paging', 'sort_by'),
    Input('datatable-paging', 'filter_query'))
def update_table(input_area_value, input_om_value, input_posto_value, input_quadro_value, input_especialidade_value,
                 page_current, page_size, sort_by, filter):
    filtered_df_tp_atual = dfTpHist[dfTpHist['ANO'] == ano_atual]

    # filtrando DF pela AREA
    if input_area_value is not None and input_area_value != '' and input_area_value != []:
        filtered_df_tp_atual = filtered_df_tp_atual.loc[filtered_df_tp_atual['COMANDO'].isin(input_area_value)]
    # filtrando DF pela OM
    if input_om_value is not None and input_om_value != '' and input_om_value != []:
        filtered_df_tp_atual = filtered_df_tp_atual.loc[filtered_df_tp_atual['UNIDADE'].isin(input_om_value)]
    # filtrando DF pela POSTO
    if input_posto_value is not None and input_posto_value != '' and input_posto_value != []:
        filtered_df_tp_atual = filtered_df_tp_atual.loc[filtered_df_tp_atual['POSTO'].isin(input_posto_value)]
    # filtrando DF pela QUADRO
    if input_quadro_value is not None and input_quadro_value != '' and input_quadro_value != []:
        filtered_df_tp_atual = filtered_df_tp_atual.loc[filtered_df_tp_atual['QUADRO'].isin(input_quadro_value)]
    # filtrando DF pela ESPEC
    if input_especialidade_value is not None and input_especialidade_value != '' and input_especialidade_value != []:
        filtered_df_tp_atual = filtered_df_tp_atual.loc[filtered_df_tp_atual['ESPEC'].isin(input_especialidade_value)]

    # adequando df para exibição na tabela
    filtered_df_tp_atual.insert(0, "indice", range(1, len(filtered_df_tp_atual) + 1), True)
    dff = filtered_df_tp_atual
    # criar coluna status
    dff['STATUS'] = dff.apply(achar_status, axis=1)
    # aplicando filtro da tabela
    filtering_expressions = filter.split(' && ')
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)
        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]
    # aplicando ordenação da tabela
    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )

    page = define_page_current(len(dff), PAGE_SIZE, page_current)
    size = page_size
    # aplicando coluna de indice para melhor visualização da quantidade de itens
    dff['indice'] = range(1, len(dff) + 1)
    return dff.iloc[page * size: (page + 1) * size].to_dict('records'), define_page_count(len(dff), PAGE_SIZE)


def define_page_count(total_elementos, quantidade_por_pagina):
    num_paginas = ceil(total_elementos / quantidade_por_pagina)
    if num_paginas == 0:
        return 1
    return num_paginas


def define_page_current(total_elementos, quantidade_por_pagina, page_current_atual):
    num_paginas = ceil(total_elementos / quantidade_por_pagina)
    if num_paginas < page_current_atual:
        return 0
    return page_current_atual


def achar_status(registro):
    if (registro['Dif(EXI)'] < 0) & (registro['Dif(EXI+PTTC)'] < 0):
        return '🔴'
    elif (registro['Dif(EXI)'] < 0) & (registro['Dif(EXI+PTTC)'] >= 0):
        return '🔶'
    else:
        return '🔵'

