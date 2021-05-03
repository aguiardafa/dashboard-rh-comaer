# Importando as bibliotecas necessárias para o projeto
import dash_bootstrap_components as dbc
import dash_html_components as html

from dashboard import tab1, tab2

# MONTAGEM GERAL DO DASHBOARD
layout = dbc.Jumbotron(children=[
    dbc.Row(  # CARDS EM LINHA
        [
            html.Div([html.Img(src='/assets/logo.png')], style={'padding-right': '15px'}),
            dbc.Col([
                html.H1(children='Comando da Aeronáutica',
                        style={'textAlign': 'left'}, className="display-4"),
                html.P("Dashboard das informações de Recursos Humanos do COMAER", className="lead")
                ]
            )
        ],
        no_gutters=True
    ),
    html.Hr(),
    dbc.Tabs(
        id="tabs",
        active_tab="tab-1",
        children=[
            dbc.Tab(tab1.tab1_content, label="Tabela de Pessoal", tab_id="tab-1"),
            #dbc.Tab(tab2.tab2_content, label="Entradas e Saídas", tab_id="tab-2"),
        ],
    )
], style={'padding-top': '0.5rem'})
