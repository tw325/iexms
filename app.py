from dash.dependencies import Input, Output
import dash
import dash_core_components as dcc
import dash_html_components as html

#LOCAL IMPORTS
import iexms, layout

SYMBOLS = []
filename = 'symbols.txt'
with open(filename, 'r') as f:
    SYMBOLS = f.read().rstrip().split(",")
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
TYPES = ['quote', 'news', 'chart']
REQUEST_TIMEOUT = 5.0

PARAMS = {
    'symbols': ','.join(SYMBOLS), # TODO
    'types': ','.join(TYPES),
    'range': '1m',
    'last': '5'
}

batch_json = iexms.get_batch(PARAMS, REQUEST_TIMEOUT)
most_active_json = iexms.get_most_active(REQUEST_TIMEOUT)
sector_performance_json = iexms.get_sector_performance(REQUEST_TIMEOUT)
symbols_json = iexms.get_symbols(REQUEST_TIMEOUT)
options = [{'label': s['symbol'], 'value': s['symbol']} for s in symbols_json]

################################### ACTUAL APP #################################

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='IEX Management System'),

    html.Div([

        html.Div([
            html.H6(children='Sector Performance'),
            layout.table(sector_performance_json, 'sector_performance', ['name','performance']),
        ], className="three columns"),

        html.Div([
            html.Div(id='my-div'),
            dcc.Dropdown(
                id = "dropdown",
                options=options,
                value=SYMBOLS,
                multi=True
            ),

            html.H4(children='Your Watchlist'),
            dcc.Tabs(
                id="tabs",
                value=SYMBOLS[0],
                children=layout.tabs(SYMBOLS),
            ),
            html.Div(id='tabs-content'),

            html.H4(children='All'),
            layout.chart_graph_layered(batch_json, 'lines'),
        ], className="five columns"),

        html.Div([
            html.H6(children='Stock Symbols'),
            layout.table_all(most_active_json, 'most_active', 10),
        ], className="four columns"),


    ], className="row "),

], style={'textAlign': 'center'})

@app.callback(Output('tabs-content', 'children'), [Input('tabs', 'value')])
def render_content(tab):
    # return layout.chart_graph(batch_json, tab, 'lines')
    return layout.news_table(batch_json[tab]["news"], tab, ['datetime', 'source', 'headline', 'url'])

@app.callback(Output('my-div', 'children'), [Input('dropdown', 'value')])
def update_output_div(input_value):
    f = open(filename, 'w')
    s = f.write(','.join(input_value))
    f.close()
    return 'You\'ve entered "{}"'.format(','.join(input_value))

if __name__ == '__main__':
    app.run_server(debug=True)
