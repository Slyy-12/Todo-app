from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd


app = Dash()

df = pd.read_csv('New_heatsink_6-10Dec.csv')

fig = px.scatter(df, x="Time", y="Voltage",
                 size="Date", color="Unit",
                 log_x=True, size_max=60)

app.layout = html.Div([
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run(debug=True)