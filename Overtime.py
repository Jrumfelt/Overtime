"""
File: Overtime.py
Author: Joseph Rumfelt
Email: jrumfelt1213@gmail.com
Phone: (518)414-1483
Purpose: Determine Overtime position priority for Schenectady PD
"""
from csv import *
import wx
import pandas as pd

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
                        "id" : line[0],
                        "first" : line[1], 
                        "second" : line[2],
                        "job" : line[3],
                        "totalovertime" : line[4],
                        "8hours" : line[5],
                        "4hours" : line[6],
                        "overtimerank" : line[7],
                        "previousposition": line[8]
                        }
            dictall[line[0]] = dicttemp
        f_object.close()
    return dictall

#Takes a list of employee IDs and calculates their overtime priority rank based on who is higher in Names.csv and job position.
#Returns a ***LIST/DICTIONARY*** with the employee information and rank
def rank(ids):
    tempposition = 0
    fieldofficers = {}
    detectives = {}
    dictall = viewall()
    for key, value in dictall.items():
        tempposition += 1
        if key in ids:
            value["previousposition"] = tempposition
            if value["job"] == "FieldOfficer":
                fieldofficers[key] = value
            elif value["job"] == "Detective":
                detectives[key] = value
            else:
                print("ERROR: Job Position Not Recognized For:" + value["first"] + " " + value["second"] + " " + value["id"])
    rank = 0
    rankedlst = []
    for key, value in fieldofficers.items():
        rank += 1
        value["overtimerank"] = rank
        rankedlst.append(fieldofficers[key])
    for key, value in detectives.items():
        rank += 1
        value["overtimerank"] = rank
        rankedlst.append(detectives[key])
    return rankedlst
    
#Change the preferred hours for 8 and 4 hour overtime blocks for a given employee id 
def changehours(id, eighthour, fourhour):
    r = reader(open(fname))
    lines = list(r)
    for line in lines:
        if line[0] == id:
            line[5] = eighthour
            line[6] = fourhour
            break
    print(lines)
    #TODO: Add writer that doesnt delete everything
    
#Shift row to bottom of csv to reset their rank priority     
def shiftlast(id):
    #TODO: Everything here
    return None

#Home tab of application that shows buttons to switch to other tabs as well as the list of employees
class TabHome(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "Overtime Priority Ranking", (20,20))

#Tab for adding new employees. Has field for name, number, and job position of new employee
class TabNewEmployee(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "New Employee", (20,20))
        
        
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
    #init wx app
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()
    
if __name__ == "__main__":
    main()
