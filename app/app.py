import flask
import dash
import dash_bootstrap_components as dbc

flask_app = flask.Flask(__name__)

dash_app = dash.Dash(__name__, title='Dashboard Recursos Humanos COMAER', server = flask_app, url_base_pathname = '/', external_stylesheets = [dbc.themes.CERULEAN], suppress_callback_exceptions = True)

server = dash_app.server
