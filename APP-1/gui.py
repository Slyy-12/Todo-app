import functions 

import FreeSimpleGUI as sg

label = sg.Text("Type in a to-do")
input_box = sg.InputText(tooltip="Enter todo")
add_button = sg.Button("Add")
edit_button = sg.Button("Edit")
complete_button = sg.Button("Complete")
exit_button = sg.Button("Exit")

window = sg.Window('My Todo-App', layout=[[[label], [input_box, add_button], [edit_button], [exit_button], [complete_button]]])
window.read()
window.close()
