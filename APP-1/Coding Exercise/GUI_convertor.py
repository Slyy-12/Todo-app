import FreeSimpleGUI as sg

label1 = sg.Text("Enter feet:")
label2 = sg.Text("Enter inches:")
user_input1 = sg.Input()
user_input2 = sg.Input()
button1 = sg.Button("Convert")

window = sg.Window("Convertor", layout=([label1, user_input1],[label2, user_input2], [button1]))

while True:

    event, values = window.read()
    print(event, values)

    window.close()