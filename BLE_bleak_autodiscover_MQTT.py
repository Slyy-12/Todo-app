import random
from bleak import BleakScanner, BleakClient, BleakError
import DMMdecoder
import asyncio
import csv
#import dash_daq as daq
from time import sleep, strftime, time
#based of the script from https://justanotherelectronicsblog.com/?p=930
import paho.mqtt.client as mqtt

hostname = "broker.emqx.io"
broker_port = 1883
topic = "raspberry"

client = mqtt.Client()

client.on_Connect = "on_connect"
client.on_message = "on_message"

client.connect(hostname, broker_port, 60)


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
    #print (DMM_data)
    DMM_ID = DMM_data['typeID']
    Display = DMM_data["display"]
    Value = DMM_data["value_type"]
    Icons = DMM_data["icons"]
    write.writerow([DMM_ID, Display, Value, Icons]) 
    print(DMM_ID, Display, Value)
    message = (Display) 
    client.publish(topic, message)
    #do something with the data

    #print("DMM ID: ", DMM_data["typeID"])
    #print("Display: ", DMM_data["display"])
    #print("Value type: ", DMM_data["value_type"])
    #print("Icons: ",DMM_data["icons"])

# Timestamp Logging 
#with open("/home/Life_Test/Bluetooth-DMM.py-main/Bluetooth-DMM.py-main/results.csv", "a") as log:
#    while True:
#        log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(DMM_UUID)))    
        


if __name__ == "__main__":
    loop = asyncio.get_event_loop()  
    file = open('results.csv', 'w+')
    write = csv.writer(file)
    loop.set_debug(False)
     
    loop.run_until_complete(run())
    csvfile.close()
