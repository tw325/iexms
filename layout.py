import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

#LOCAL IMPORTS
import iexms

def dcc_graph(id, data, layout):
    return dcc.Graph(
        id=id,
        figure={
            'data': data,
            'layout': layout
        }
    )

def go_layout():
    return go.Layout(
        height = 400,
        xaxis={'title': 'Date'},
        # yaxis={'title': 'Price'},
        margin={'l': 50, 'b': 50, 't': 50, 'r': 50, 'pad': 4},
        legend={'x': 0, 'y': 1},
        hovermode='closest'
    )

def go_scatter(name_df, name, mode):
    return go.Scatter(
        x=[i for i in range(len(name_df))],
        y=[name_df.iloc[i]['open'] for i in range (len(name_df))],
        mode=mode,
        opacity=0.7,
        marker={
            'size': 10,
            'line': {'width': 0.5, 'color': 'white'}
        },
        name=name
    )

def html_div_center(children, width):
    return html.Div(
        children= children,
        style={'margin':'0 auto', 'width': width,}
    )

def html_table(json, max_rows=10):
    dataframe = pd.DataFrame.from_dict(json)
    return html.Table(
        [html.Tr([html.Th(col) for col in dataframe.columns])] +
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

def news_table(batch_json, name):
    return html_table(batch_json[name]["news"], max_rows=10)

def chart_graph(batch_json, name, mode):
    name_df = pd.DataFrame.from_dict(batch_json[name]["chart"])
    return dcc_graph(name, [go_scatter(name_df, name, mode)], go_layout())

def chart_graph_layered(batch_json, mode):
    data = []
    for name, value in batch_json.items():
        name_df = pd.DataFrame.from_dict(batch_json[name]["chart"])
        data.append(go_scatter(name_df, name, mode))
    return dcc_graph(name, data, go_layout())

def tabs(symbols_json):
    return [dcc.Tab(label=s, value=s) for s in symbols_json]
