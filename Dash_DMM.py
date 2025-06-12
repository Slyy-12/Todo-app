import DMMdecoder
import json
from dash import Dash, html, dcc, Input, Output, callback
import dash_daq as daq
import random


def notification_handler(sender, data):
    DMM_data = DMMdecoder.decode(data.hex(" "))
    #print(type(DMM_data))
    
    y = json.dumps(DMM_data)
    print (DMM_data)
    #DMM_ID = DMM_data['typeID']
    Display = DMM_data["Value"]
    print(Display)
    #Value = DMM_data["value_type"]
    # Icons = DMM_data["Mode"]

app = Dash()

app.layout = html.Div([
    daq.LEDDisplay(
        id='my-LED-display-1',
        label="Voltage",
        color="#FF5E5E",
        labelPosition="top",
        size=64,
        value=6
    ),
        daq.LEDDisplay(
        id='my-LED-display-2',
        label="Current",
        labelPosition='top',
        color="#FF5E5E",
        size=64,
        value=6
    ),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
])

@callback(
    Output('my-LED-display-1', 'value'),
    Input('interval-component', 'n_intervals')
)
def update_output(value):
    x = random.randint(0,100)
    value= x
    return (value)

@callback(
    Output('my-LED-display-2', 'value'),
    Input('interval-component', 'n_intervals')
)
def update_output(value):
    x = random.randint(0,100)
    value= x
    return (value)

if __name__ == '__main__':
    app.run(debug=True)