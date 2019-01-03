from dash.dependencies import Input, Output
import dash
import dash_core_components as dcc
import dash_html_components as html

#LOCAL IMPORTS
import iexms, layout

filename = 'symbols.txt'
with open(filename, 'r') as f:
    SYMBOLS = f.read().rstrip().split(",")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
TYPES = ['quote', 'news', 'chart']
LIST_TYPES = ['mostactive', 'gainers', 'losers', 'iexvolume', 'iexpercent', 'infocus']
REQUEST_TIMEOUT = 5.0
sector_performance_json = iexms.get_sector_performance(REQUEST_TIMEOUT)
symbols_json = iexms.get_symbols(REQUEST_TIMEOUT)
options = [{'label': s['symbol'], 'value': s['symbol']} for s in symbols_json]

def generate_params(symbols, types):
    d = {
        'types': ','.join(types),
        'range': '1m',
        'last': '5'
    }
    if len(symbols) > 0:
        d['symbols'] = ','.join(symbols)
    return d

def update_symbols(input_value):
    SYMBOLS = input_value
    with open(filename, 'w') as f:
        f.write(','.join(input_value))

################################### ACTUAL APP #################################

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config['suppress_callback_exceptions']=True

app.layout = html.Div(children=[
    html.H2(children='IEXMS'),

    html.Div([

        html.Div([
            layout.tabs('list', LIST_TYPES),
            html.Div(id='list-content'),
        ], className="twelve columns"),

    ], className="row "),

    html.Div([

        html.Div([
            html.H6(children='Watchlist'),
            dcc.Dropdown(
                id = "dropdown",
                options=options,
                value=SYMBOLS,
                multi=True
            ),
            html.Div(id='graph-all'),
        ], className="eight columns"),

        html.Div([
            html.H6(children='Sector Performance'),
            layout.table(sector_performance_json, 'sector_performance', ['name','performance']),
        ], className="four columns"),

    ], className="row "),

    html.Div([

        html.Div([
            html.Div(id = 'my-stocks'),
            html.Div(id = 'tabs'),
            html.Div(id='tabs-news'),
            html.Div(id='tabs-graph'),
        ], className="twelve columns"),

    ], className="row "),

], className = "container", style={'textAlign': 'center'})

@app.callback(Output('tabs', 'children'), [Input('dropdown', 'value')])
def render_tabs(input_value):
    update_symbols(input_value)
    return layout.tabs("my-tabs", input_value)

@app.callback(Output('graph-all', 'children'), [Input('dropdown', 'value')])
def render_graph_all(input_value):
    batch_json = iexms.get_batch(generate_params(input_value,TYPES), REQUEST_TIMEOUT)
    return layout.chart_graph_layered(batch_json, 'lines'),

@app.callback(Output('tabs-news', 'children'), [Input('my-tabs', 'value')])
def render_news(tab):
    stock_json = iexms.get_stock(tab, generate_params([], TYPES), REQUEST_TIMEOUT)
    return layout.chart_graph(stock_json, tab, 'lines')

@app.callback(Output('tabs-graph', 'children'), [Input('my-tabs', 'value')])
def render_graph_stock(tab):
    stock_json = iexms.get_stock(tab, generate_params([], TYPES), REQUEST_TIMEOUT)
    return layout.news_table(stock_json["news"], tab, ['datetime', 'source', 'headline', 'url'])

@app.callback(Output('list-content', 'children'), [Input('list', 'value')])
def render_list(tab):
    json = iexms.get_list(tab, REQUEST_TIMEOUT)
    return layout.table_all(json, tab, 10)

if __name__ == '__main__':
    app.run_server(debug=True)
