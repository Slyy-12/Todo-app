import random 
import json
from bleak import BleakScanner, BleakClient, BleakError
import DMMdecoder
import asyncio
import csv
from time import sleep, strftime, time
# import paho.mqtt.client as mqtt
from datetime import datetime
import tempfile 

from dash import Dash, html, dcc, Input, Output, callback
import dash_daq as daq

#MQTT Information 
# hostname = "172.17.108.180"
# broker_port = 1883
# topic = "raspberry"

# client = mqtt.Client()

# client.on_Connect = "on_connect"
# client.on_message = "on_message"

# client.connect(hostname, broker_port, 60)


device_name = "Bluetooth DMM"
DMM_UUID = "0000fff4-0000-1000-8000-00805f9b34fb" 

def on_disconnect(client, *args, **kwargs):
    print("Disconnected from device.")
    exit()

async def run():
    print("Scanning for devices...")
    address = await BleakScanner.find_device_by_filter(filterfunc =(lambda d, ad: d.name == device_name), timeout=20.0)
    if not address:
        print("Device with name " + device_name + " not found!")
        exit()
    
    print("Found "+ address.name + ", Address: " + address.address + "!")
    
    async with BleakClient(address, disconnected_callback=on_disconnect) as client:
        while True:
            await client.start_notify(DMM_UUID, notification_handler)
            await asyncio.sleep(5.0)
            await client.stop_notify(DMM_UUID)

def notification_handler(sender, data):
    DMM_data = DMMdecoder.decode(data.hex(" "))
    #print(type(DMM_data))
    
    y = json.dumps(DMM_data)
    # print (DMM_data)
    #DMM_ID = DMM_data['typeID']
    Display = DMM_data["Value"]
    Display_int = int(Display)
    # print(type(Display))
    #Value = DMM_data["value_type"]
    # Icons = DMM_data["Mode"]
    
    # now = datetime.now()
    # time = now.strftime("%H:%M")
    # date = now.strftime("%m/%d/%Y") 
    # write.writerow([time, date, Display, Icons]) 
    # #print(DMM_ID, Display, Value)
    
    # message = (y)
    
    # client.publish(topic, message)

app = Dash()

app.layout = html.Div([
    daq.LEDDisplay(
        id='my-LED-display-1',
        label="Default",
        value=1
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
    DMM_data = DMMdecoder.decode(data.hex(" "))
    y = json.dumps(DMM_data)
    Display = DMM_data["Value"]
    Display_int = int(Display)
    value= Display_int 
    return (value)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()  
    app.run(debug=True)
    file_name = tempfile.NamedTemporaryFile(prefix="Results_", suffix=".csv", dir=".", delete=False)
    file = open(file_name.name, 'w')
    write = csv.writer(file)
    loop.set_debug(False)
     
    loop.run_until_complete(run())
    csvfile.close()

if __name__ == '__main__':
    app.run(debug=True)