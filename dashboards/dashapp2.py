from pprint import pprint
import sys,os,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from .main import apply_layout_with_auth
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
from pprint import pprint
import dash_bootstrap_components as dbc
from multiprocessing import Pool

url_base = '/dash/app2/'
class Dash_app2:
    def __init__(self,server, layout=None):
        self.server = server
        self.layout = layout

    def get_dash_app(self):
        print('Вызов get_dash_app')
        app = dash.Dash(server=self.server, url_base_pathname=url_base,external_stylesheets=[dbc.themes.BOOTSTRAP])

        layout = html.Div([
          dcc.Input(
            id="input",
            className = 'form-control',
            placeholder="На звание вашего git gist",
            style = {'margin-bottom':10}
        ),
            dcc.Textarea(
                id='textarea-example',
                style={'width': '50%', 
                       'height': '100%',
                       'position':'absolute',
                       'left':0,
                       'padding':10},
                className = 'form-control'
            ),
            dcc.Markdown(id='textarea-example-output', style={'whiteSpace': 'pre-line',
                                                              'width':'50%',
                                                              'position':'absolute',
                                                              'right':0,
                                                              'height': '100%',
                                                              'overflow':'scroll',
                                                              'padding':10
                                                              },
                        className = 'form-control',
                        highlight_config = 'dark')
        ])
        @app.callback(
            Output('textarea-example-output', 'children'),
            Input('textarea-example', 'value')
        ) 
        def update_output(value):
            return '{}'.format(value)
        apply_layout_with_auth(app, layout)

        return app.server

