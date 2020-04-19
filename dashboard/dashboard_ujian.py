import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

df = pd.read_csv('auto_imports_ujian.csv')
df_plot = df.copy()

## CDN CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# execute Dash in python 
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def generate_table(dataframe, page_size=10):
    return dash_table.DataTable(
        id= 'dataTable',
        columns=[{'name': i ,'id' : i} for i in dataframe.columns],
        data = dataframe.to_dict('records'),
        style_table= {'overflowX' : 'scroll'},
        page_action ='native',
        page_current = 0,
        page_size=page_size
    )

app.layout = html.Div([
    html.H1('Ujian Modul 2 Dashboard Auto Imports'),
    html.P('Created by : Alvin Hizra Muhammad'),
    html.Div([
        html.Div(children=[
            dcc.Tabs(value='tabs', id='tabs-1', children=[
                dcc.Tab(value='Tabel', label='DataFrame Table', children=[
                    html.Center(html.H1('Dataframe TSA')),
                    html.Div(children=[generate_table(df)])
                ]),
                dcc.Tab(label='Bar-Chart', value='tab-satu',children=[
                    html.Div(children=[
                        html.Div(children=[
                            html.P('Y1 :'),
                            dcc.Dropdown(id='y-axis-1', options=[{'label':i,'value':i} for i in df_plot.select_dtypes('number').columns],
                            value='Wheel-Base')
                        ], className='col-4'),
                        html.Div(children=[
                            html.P('Y2 :'),
                            dcc.Dropdown(id='y-axis-2', options=[{'label':i,'value':i} for i in df_plot.select_dtypes('number').columns],
                            value='Length')
                        ], className='col-4'),
                        html.Div(children=[
                            html.P('X :'),
                            dcc.Dropdown(id='x-axis-1', options=[{'label':i,'value':i} for i in df_plot.select_dtypes('object').columns],
                            value='Drive-Wheels')
                        ], className='col-4'),
                        
                        html.Div([
                            dcc.Graph(
                                id='graph-bar',
                                figure= {
                                    'data' : [
                                        {'x' : df_plot['Drive-Wheels'], 'y' : df_plot['Wheel-Base'], 'type' : 'bar', 'name': 'Wheel-Base'},
                                        {'x' : df_plot['Drive-Wheels'], 'y' : df_plot['Length'], 'type' : 'bar', 'name': 'Length'}
                                    ],
                                    'layout' : {'title' : 'Bar Chart'}
                                }
                            )
                        ])
                    ]),
            ]),
            dcc.Tab(label='Scatter-Chart', value='tab-dua', children=[
                    html.Div(children= dcc.Graph(
                        id='graph-scatter',
                        figure={'data' : [
                            go.Scatter(
                                x = df_plot[df_plot['Drive-Wheels'] == i]['Horsepower'],
                                y = df_plot[df_plot['Drive-Wheels'] == i]['Price'],
                                mode='markers',
                                name='{}'.format(i)
                            ) for i in df_plot['Drive-Wheels'].unique() 
                        ],
                        'layout' : go.Layout(
                            xaxis={'title' : 'Horsepower'},
                            yaxis={'title' : 'Price'},
                            hovermode='closest'
                        )
                        }
                    ))
                ]),
            dcc.Tab(label = 'Pie-Chart', value='tab-tiga', children=[
                html.Div(dcc.Dropdown(id='pie-dropdown', options=[{'label':i,'value':i} for i in df_plot.select_dtypes('number').columns],value='Price'),
                className='col-4'),
                html.Div([
                    dcc.Graph(
                        id='graph-pie',
                        figure={
                            'data': [
                                go.Pie(labels=['{}'.format(i) for i in list(df_plot['Fuel-System'].unique())],
                                values=[df_plot.groupby('Fuel-System').mean()['Price'][i] for i in list(df_plot['Fuel-System'].unique())],
                                sort= False
                                )
                            ],
                            'layout' : {'title' : 'Mean Pie Chart'}
                        }
                    )
                ])
            ])
            ])
        ])
    ])
])

# Bar chart
@app.callback(
    Output(component_id='graph-bar', component_property='figure'),
    [Input(component_id='y-axis-1', component_property='value'),
    Input(component_id='y-axis-2', component_property='value'),
    Input(component_id='x-axis-1', component_property='value')]
)

def create_graph_bar(y1,y2,x1):
    figure = {
        'data' : [
            {'x' : df_plot[x1], 'y' : df_plot[y1], 'type' : 'bar', 'name' : y1},
            {'x' : df_plot[x1], 'y' : df_plot[y2], 'type' : 'bar', 'name' : y2}
        ],
        'layout' : {'title' : 'Bar Chart'}
    }
    return figure

# Pie Chart
@app.callback(
    Output(component_id='graph-pie', component_property='figure'),
    [Input(component_id='pie-dropdown', component_property='value')]
)

def create_graph_pie(columns):
    figure = {
        'data' : [
            go.Pie(labels=['{}'.format(i) for i in list(df_plot['Fuel-System'].unique())],
            values=[df_plot.groupby('Fuel-System').mean()[columns][i] for i in list(df_plot['Fuel-System'].unique())],
            sort= False
            )
        ],
        'layout' : {'title' : 'Mean Pie Chart'}
    }
    return figure

if __name__ == '__main__':
    app.run_server(debug=True, port=2211)