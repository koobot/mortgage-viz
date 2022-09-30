# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import json
import numpy as np
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

# DATA ----------------------------------------------------------------
# Deposit values
deposit_percent = np.arange(0.10, 0.20 + 0.01, 0.01)
deposit_amount = np.arange(100e3, 200e3 + 20e3, 20e3)

# Input e.g. 5.5% = 0.055
stamp_duty = 0.055

# Create data frame
# deposit amount * deposit percent
house_price = (
    pd.MultiIndex
        .from_product(
            [deposit_amount, deposit_percent],
            names=('deposit_amount', 'deposit_percent'))
        .to_frame()
        .reset_index(drop=True)
)

# Calculate
house_price['purchase_price'] = house_price['deposit_amount'] / house_price['deposit_percent']
house_price['principal_amount'] = house_price['purchase_price'] - house_price['deposit_amount']
house_price['stamp_duty'] = house_price['purchase_price'] * stamp_duty
house_price['amount_ready'] = house_price['deposit_amount'] + house_price['stamp_duty']

# Reorder columns
house_price = house_price[[
    'amount_ready',
    'deposit_amount',
    'deposit_percent',
    'principal_amount',
    'purchase_price',
    'stamp_duty']]

# DASH APP ----------------------------------------------------------------
# Markdown text
intro_text = '''
# House deposit calculations

- Deposit amount is the amount saved up
- Principal amount is the amount owed to the bank before interest
- Purchase price is the total price of the house
- Amount ready = deposit + stamp duty
- Stamp duty amount: {}%

## Filter table

Use the ```Write to filter_query``` radio button to write more advanced queries.

Example query:
```
({{deposit_amount}} > 500e3 and {{deposit_amount}}) < 700e3 or {{deposit_percent}} < 0.15
```
'''

money = dash_table.FormatTemplate.money(2)
percentage = dash_table.FormatTemplate.percentage(2)

app = Dash(__name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.Div(dcc.Markdown(intro_text.format(stamp_duty*100))),

    dcc.RadioItems(
        [{'label': 'Read filter_query', 'value': 'read'},
         {'label': 'Write to filter_query', 'value': 'write'}],
        'read',
        id='filter-query-read-write',
    ),

    html.Br(),

    dcc.Input(id='filter-query-input', placeholder='Enter filter query'),

    html.Div(id='filter-query-output'),

    html.Hr(),

    dash_table.DataTable(
        id='house-prices-datatable',
        columns=[
            {'name': 'Amount ready', 'id': 'amount_ready', 'type': 'numeric', 'format': money},
            {'name': 'Deposit amount', 'id': 'deposit_amount', 'type': 'numeric', 'format': money},
            {'name': 'Deposit percent', 'id': 'deposit_percent', 'type': 'numeric', 'format': percentage},
            {'name': 'Principal amount', 'id': 'principal_amount', 'type': 'numeric', 'format': money},
            {'name': 'Purchase price', 'id': 'purchase_price', 'type': 'numeric', 'format': money},
            {'name': 'Stamp duty', 'id': 'stamp_duty', 'type': 'numeric', 'format': money}
        ],
        data=house_price.to_dict('records'),
        filter_action='native',
        page_action='native',
        page_size=10,
        style_table={
            'height': 400,
        },
        style_data={
            'width': '150px', 'minWidth': '150px', 'maxWidth': '150px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(220, 220, 220)',
            }
        ],
        style_header={
            'backgroundColor': 'rgb(210, 210, 210)',
            'color': 'black',
            'fontWeight': 'bold'
        }
    ),
    html.Hr(),
    html.Div(id='datatable-query-structure', style={'whitespace': 'pre'})
])

# Input and Output
@app.callback(
    Output('filter-query-input', 'style'),
    Output('filter-query-output', 'style'),
    Input('filter-query-read-write', 'value')
)
def query_input_output(val):
    input_style = {'width': '100%'}
    output_style = {}
    if val == 'read':
        input_style.update(display='none')
        output_style.update(display='inline-block')
    else:
        input_style.update(display='inline-block')
        output_style.update(display='none')
    return input_style, output_style

@app.callback(
    Output('house-prices-datatable', 'filter_query'),
    Input('filter-query-input', 'value')
)
def write_query(query):
    if query is None:
        return ''
    return query

@app.callback(
    Output('filter-query-output', 'children'),
    Input('house-prices-datatable', 'filter_query')
)
def read_query(query):
    if query is None:
        return "No filter query"
    return dcc.Markdown('`filter_query = "{}"`'.format(query))

@app.callback(
    Output('datatable-query-structure', 'children'),
    Input('house-prices-datatable', 'derived_filter_query_structure')
)
def display_query(query):
    if query is None:
        return ''
    return html.Details([
        html.Summary('Derived filter query structure'),
        html.Div(dcc.Markdown('''```json
{}
```'''.format(json.dumps(query, indent=4))))
    ])

if __name__ == '__main__':
    app.run_server(debug=True)