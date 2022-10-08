import pandas as pd
import plotly.express as px
import dash
from dash import Dash, html, dcc, Input, Output

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='AEP'), 
    html.Div(children=[
        html.Label('Dropdown'),
        dcc.Dropdown(['Total', 'Station A', 'Station B', "Station C", "Station D", "Station E", "Station F", "Station G", "Station H", "Station I", "Station J"], "Total")
    ])
    ,

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)

if __name__ == '__main__':
    app.run_server(debug=True)