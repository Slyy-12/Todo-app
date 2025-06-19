import FreeSimpleGUI as sg
from feet_convertor import convert

label1 = sg.Text("Enter feet:")
label2 = sg.Text("Enter inches:")
user_input1 = sg.Input(key="feet")
user_input2 = sg.Input(key="inches")
convert_button = sg.Button("Convert")
output_label = sg.Text(key="output")
window = sg.Window("Convertor", layout=([label1, user_input1],[label2, user_input2], [convert_button, output_label]))

while True:

    event, values = window.read()
    # print(event, values)
    feet = float(values["feet"])
    inches = float(values["inches"])
    result = convert(feet, inches)
    window["output"].update(value=f"{result} m")

window.close()