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
from yapi.api import Api,Graph
import dash_bootstrap_components as dbc
url_base = '/dash/app1/'
class SaveGraph:
    def __get__(self,instance, owner):
        return self.__value

    def __set__(self, instance, value):
        self.__value = value

    def __delete__(self,obg):
        del self.__value

# layout - это та разметка которая будет выведена в браузере  
layout = html.Div([
            dcc.Input(id='pattern', type='text'), 
            html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
            html.Div(id='output-state')
        ])

class Layout:
    layout  = SaveGraph()

    def __init__(self,fig=None):
        self.layout = None
        self.fig = fig

    

        layout = html.Div([
            dcc.Graph(
                id='example-graph',
                figure={
                }

            )
        ])
           
        self.layout = layout

class Dash_app:
    def __init__(self,server, layout=None):
        self.server = server
        self.layout = layout

    def get_dash_app(self):
        app = dash.Dash(server=self.server, url_base_pathname=url_base,external_stylesheets=[dbc.themes.BOOTSTRAP])
        graph = Graph()

        input_types = ['number', 'password', 'text', 'tel', 'email', 'url', 'search', 'hidden']
        layout = html.Div([
            dbc.Input(id="pattern",  type="text"),
            dbc.Button(id="submit-button-state",n_clicks=0, color="primary mt-2",children='Найти', className="mr-1"),
            dcc.Graph(id="bar-chart"),
        ])
        @app.callback(Output('bar-chart', 'figure'),
              Input('submit-button-state', 'n_clicks'),
              State('pattern', 'value'))
        def update_output(n_clicks,input1):
            fig = graph.make_graph(input1)
            return fig
           
        apply_layout_with_auth(app, layout)

        return app.server

    # def make_loyout(self):
        

    #     layout = html.Div([
    #         dbc.Input(id="input", placeholder="Type something...", type="text"),
    #         dcc.Graph(id="bar-chart"),
    #     ])
        # return layout

    

# layout = html.Div([
    
#     html.Div('URL'),
#     dcc.Input(id='url'), html.Br(), html.Br(),
#     html.Div('Количество комментариев'),
#     dcc.Input(id='count'), html.Br(), html.Br(),
#     html.Button(id='my-button', n_clicks=0, children="Show breakdown"),
#     html.Div('Фильтр'),
#     dcc.Input(id = 'input_text'), html.Br(), html.Br(),
#     dbc.Alert("This is a primary alert", color="primary",id='target'),
# ])

# def Add_Dash(server):
#     app = dash.Dash(server=server, url_base_pathname=url_base)
#     apply_layout_with_auth(app, layout)

#     @app.callback(Output('output-state', 'children'),
#               Input('submit-button-state', 'n_clicks'),
#               State('pattern', 'value'))
#     def update_output(n_clicks,input1):
#         return u'''{} - {}'''.format(n_clicks,input1)

    
#     return app.server