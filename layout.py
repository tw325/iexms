import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import datetime
import dateutil.parser
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

def dt_table(id, df, n_fixed_columns=0, scroll=True):
    return dt.DataTable(
        id=id,
        css=[{
            'selector': '.dash-cell div.dash-cell-value',
            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
        }],
        style_table={'overflowX': ('scroll' if scroll else 'hidden'), 'max-width': '100%'},
        style_cell={
            'textAlign': 'left',
        },
        style_header={
            'fontWeight': 'bold'
        },
        style_cell_conditional=[{
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }],
        columns=[{"name": i, "id": i} for i in df.columns],
        n_fixed_columns = n_fixed_columns,
        data=df.to_dict("rows"),
    )

def go_layout():
    return go.Layout(
        height = 400,
        # xaxis={'title': 'Date'},
        # yaxis={'title': 'Price'},
        margin={'l': 50, 'b': 50, 't': 50, 'r': 50, 'pad': 4},
        legend=dict(orientation="h"),
        hovermode='closest'
    )

def go_scatter(name_df, name, mode):
    return go.Scatter(
        x=[datetime.date.fromisoformat(name_df.iloc[i]['date']) for i in range(len(name_df))],
        y=[name_df.iloc[i]['open'] for i in range (len(name_df))],
        mode=mode,
        opacity=0.7,
        marker={
            'size': 10,
            'line': {'width': 0.5, 'color': 'white'}
        },
        name=name,
    )

def html_div_center(children, width):
    return html.Div(
        children= children,
        style={'margin':'0 auto', 'width': width,}
    )

def html_table(dataframe, max_rows=10):
    return html.Table(
        [html.Tr([html.Th(col) for col in dataframe.columns])] +
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

def tab(symbols_json):
    return [dcc.Tab(
        label=s,
        value=s,
        style={'padding': '6px'},
        selected_style={'padding': '6px'}
        ) for s in symbols_json]

def tabs(id, input):
    return dcc.Tabs(
        id = id,
        value=input[0],
        children=tab(input),
    )

########################## SUBTABLES FUNCTIONS #################################
# DASH CURRENTLY DOES NOT SUPPORT THE USE OF URL IN DATATABLE.
# https://community.plot.ly/t/datatable-column-clickalbe-to-link-to-url/14680/2
def news_table(news_json, name, fields):
    for article in news_json:
        date = dateutil.parser.parse(article['datetime'])
        article['datetime'] = date.strftime("%a %b %d, %I:%M%p")
    df = pd.DataFrame.from_dict(news_json)
    dataframe = df.loc[:, fields]
    return dt_table('news_table', dataframe, 0, True)

def table(json, name, fields, max_rows=10):
    df = pd.DataFrame.from_dict(json)
    dataframe = df.loc[:, fields]
    return dt_table(name, dataframe)

def table_all(json, name, max_rows=10):
    df = pd.DataFrame.from_dict(json)
    return dt_table(name, df, 0, True)

def symbols_table(symbols_json, fields, max_rows=10):
    df = pd.DataFrame.from_dict(symbols_json)
    dataframe = df.loc[:, fields]
    return dt_table('symbols_table', dataframe, 1, True)

def chart_graph(stock_json, name, mode):
    name_df = pd.DataFrame.from_dict(stock_json["chart"])
    return dcc_graph(name, [go_scatter(name_df, name, mode)], go_layout())

def chart_graph_layered(batch_json, mode):
    data = []
    for name, value in batch_json.items():
        name_df = pd.DataFrame.from_dict(batch_json[name]["chart"])
        data.append(go_scatter(name_df, name, mode))
    return dcc_graph("layered", data, go_layout())
