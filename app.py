# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import numpy as np
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


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
# Reorder columns
house_price = house_price[[
    'deposit_amount',
    'deposit_percent',
    'principal_amount',
    'purchase_price',
    'stamp_duty']]

# Generate table
def generate_table(dataframe, max_rows=10000):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


app = Dash(__name__)

app.layout = html.Div([
    html.H4(children='Deposits'),
    generate_table(house_price)
])

if __name__ == '__main__':
    app.run_server(debug=True)