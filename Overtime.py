"""
File: Overtime.py
Author: Joseph Rumfelt
Email: jrumfelt1213@gmail.com
Phone: (518)414-1483
Purpose: Determine Overtime position priority for Schenectady PD
"""
from csv import *
import PySimpleGUI as sg

fname = "Names.csv"

"""
Opens csv file in append mode and adds a new employee using file and writer object
"""
def newemployee(name, id, position):
    toAppend = [name, id, position, "", "", "", "", ""]
    with open(fname, "a", newline="") as f_object:
        csv_writer = writer(f_object)
        csv_writer.writerow(toAppend)
        f_object.close()
    
"""
Initialize program and run the PySimpleGui
"""
def main():
    sg.theme('Dark2')
    #https://pysimplegui.trinket.io/demo-programs#/layouts/swapping-window-layouts
    
    #layout for home page
    layout_home = [[sg.Text("Overtime Ranking")]]
    
    #layout for new employees
    layout_newemployee = [[sg.Text("Add new employees")],
                [sg.Text("Employee first and last name"), sg.InputText()],
                [sg.Text("Employee number"), sg.InputText()],
                [sg.Text("Employee job position"), sg.InputText()],
                [sg.Button("Submit"), sg.Button("Cancel")]]
    #Create new employee window and run event loop
    """window = sg.Window('New Employee', layout_newemployee)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        elif event == "Submit":
            name = values[0]
            id = values[1]
            position = values[2]
            newemployee(name, id, position)"""
            
    #Create layout and row of buttons to swap layouts        
    layout = [[sg.Column(layout_home, key="-Home-"), sg.Column(layout_newemployee, visible = False, key="-NewEmployee-")],
              [sg.Button('Home'), sg.Button("New Employee"), sg.Button("Exit")]]
    
    window = sg.Window("Overtime Home", layout_home)
    while True:
        event, values = window.read()
        if event in (None, "Exit"):
            break
        elif event == "New Employee":
            window[f'-Home-'].update(visible = False)
            window[f'-NewEmployee-'].update(visible = True)
        elif event == "Home":
            break
    window.close()
    
if __name__ == "__main__":
    main() 
