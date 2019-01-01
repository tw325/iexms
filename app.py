from dash.dependencies import Input, Output
import dash
import dash_core_components as dcc
import dash_html_components as html

#LOCAL IMPORTS
import iexms, layout

f = open('symbols.txt', 'r')
s = f.read().rstrip()
f.close()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
SYMBOLS = s.split(",")
TYPES = ['quote', 'news', 'chart']
REQUEST_TIMEOUT = 5.0

PARAMS = {
    'symbols': ','.join(SYMBOLS), # TODO
    'types': ','.join(TYPES),
    'range': '1m',
    'last': '5'
}

symbols_json = iexms.get_symbols(REQUEST_TIMEOUT)
chart_json = iexms.get_chart(PARAMS, REQUEST_TIMEOUT)
options = []
for s in symbols_json:
    options.append({'label': s['symbol'], 'value': s['symbol']})

################################### ACTUAL APP #################################

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='IEX Management System'),

    html.Label('Multi-Select Dropdown'),
    html.Div(id='my-div'),
    layout.html_div_center([
        dcc.Dropdown(
            id = "dropdown",
            options=options,
            value=SYMBOLS,
            multi=True
        )
    ], 600),

    layout.html_div_center([
        html.H4(children='Your Watchlist'),
        dcc.Tabs(
            id="tabs",
            value=SYMBOLS[0],
            children=layout.generate_tabs(SYMBOLS),
        ),
        html.Div(id='tabs-content')
    ], 600),

    layout.html_div_center([
        html.H4(children='All'),
        layout.generate_chart_multiple_scatter(chart_json, 'lines'),
    ], 600),

    layout.html_div_center([
        html.H4(children='Stock Symbols'),
        layout.generate_table(symbols_json, 10),
    ], 600),

], className='container', style={'textAlign': 'center'})

@app.callback(Output('tabs-content', 'children'), [Input('tabs', 'value')])
def render_content(tab):
    return layout.generate_chart_scatter(chart_json, tab, 'lines')

@app.callback(Output('my-div', 'children'), [Input('dropdown', 'value')])
def update_output_div(input_value):
    for i in input_value:
        print(i)
    return 'You\'ve entered "{}"'.format(input_value)

if __name__ == '__main__':
    app.run_server(debug=True)
