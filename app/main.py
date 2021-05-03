# Importando as bibliotecas necessárias para o projeto
import dash_html_components as html

from app import flask_app, dash_app
from dashboard import layout, navbar

# carrega o layout do App
dash_app.layout = html.Div([navbar.Navbar(), layout.layout])

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', debug=True, port=80)
