"""
File: Overtime.py
Author: Joseph Rumfelt
Email: jrumfelt1213@gmail.com
Phone: (518)414-1483
Purpose: Determine Overtime position priority for Schenectady PD
"""
from csv import *
import PySimpleGUI as sg
import wx

fname = "Names.csv"


#Opens csv file in append mode and adds a new employee using file and writer object
def newemployee(first, last, id, position):
    toAppend = [id, first, last, position, "", "", "", "", ""]
    with open(fname, "a", newline="") as f_object:
        csv_writer = writer(f_object)
        csv_writer.writerow(toAppend)
        f_object.close()
        
#Returns a dict of all employees with id as key and the values being a 
#dictionary with first name, last name, total overtime, 8hours, 4hours, overtime rank, and previous position in file   
def viewall():
    dictall = {}
    with open(fname, "r") as f_object:
        read = reader(f_object)
        for line in read:
            dicttemp = {
                        "first" : line[1], 
                        "second" : line[2],
                        "position" : line[3],
                        "totalovertime" : line[4],
                        "8hours" : line[5],
                        "4hours" : line[6],
                        "overtimerank" : line[7],
                        "previousposition": line[8]
                        }
            print(dicttemp)
            dictall[line[0]] = dicttemp
    return dictall    

#Home tab of application that shows buttons to switch to other tabs as well as the list of employees
class TabHome(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "Overtime Priority Ranking", (20,20))

#Tab for adding new employees. Has field for name, number, and job position of new employee
class TabNewEmployee(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "Add New Employee", (20,20))
        
#Mainframe
class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Overtime Priority")

        # Create a panel and notebook (tabs holder)
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        # Create the tab windows
        tabhome = TabHome(nb)
        tabnewemp = TabNewEmployee(nb)


        # Add the windows to tabs and name them.
        nb.AddPage(tabhome, "Home")
        nb.AddPage(tabnewemp, "New Employee")

        # Set noteboook in a sizer to create the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)    
    
"""
Initialize gui application
"""
def main():
    sg.theme('Dark2')
    
   #layout for new employees
    layout_newemployee = [[sg.Text("Add new employees")],
                [sg.Text("Employee first and last name"), sg.InputText()],
                [sg.Text("Employee number"), sg.InputText()],
                [sg.Text("Employee job position"), sg.InputText()],
                [sg.Button("Submit"), sg.Button("Cancel")]]
    #Create new employee window and run event loop
    window = sg.Window('New Employee', layout_newemployee)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        elif event == "Submit":
            name = values[0]
            id = values[1]
            position = values[2]
            newemployee(name, id, position)
            break
    window.close()
    
    #init wx app
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()
    
    
if __name__ == "__main__":
    main()
