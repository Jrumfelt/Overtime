"""
File: Overtime.py
Author: Joseph Rumfelt
Email: jrumfelt1213@gmail.com
Phone: (518)414-1483
Purpose: Determine Overtime position priority for Schenectady PD
"""
from csv import *
import wx
import shutil
from tempfile import NamedTemporaryFile
import datetime

fname = "Names.csv"
fields = ["id", "name", "job", "totalovertime", "8hours", "4hours", "overtimerank", "previousposition", "date"]

#Opens csv file in append mode and adds a new employee using file and writer object
def newemployee(name, id, position):
    toAppend = [id, name, position, "", "", "", "", ""]
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
            if line == []:
                print("ERROR: Empty Line in Names.csv")
                break
            dicttemp = {
                        "id" : line[0],
                        "name" : line[1], 
                        "job" : line[2],
                        "totalovertime" : line[3],
                        "8hours" : line[4],
                        "4hours" : line[5],
                        "overtimerank" : line[6],
                        "previousposition": line[7],
                        "date" : line[8]
                        }
            dictall[line[0]] = dicttemp
        f_object.close()
    return dictall

#Takes a list of employee IDs and calculates their overtime priority rank based on who is higher in Names.csv and job position.
#Returns a dictionary with the employee information and rank
def rank(ids):
    tempposition = 0
    #dictionaries of all the positions
    fsbptl = {}
    fsbsgt = {}
    fsblt = {}
    isbdet = {}
    isbsgt = {}
    isblt = {}
    asbptl = {}
    asbsgt = {}
    asblt = {}
    dictall = viewall()
    #Place in the correct dictionary if it is one of the given ids
    for key, value in dictall.items():
        tempposition += 1
        if key in ids:
            value["previousposition"] = tempposition
            if value["job"] == "FSB PTL":
                fsbptl[key] = value
            elif value["job"] == "ISB DET":
                isbdet[key] = value
            elif value["job"] == "ASB PTL":
                asbptl[key] = value
            elif value["job"] == "FSB SGT":
                fsbsgt[key] = value
            elif value["job"] == "ISB SGT":
                isbsgt[key] = value
            elif value["job"] == "ASB SGT":
                asbsgt[key] = value
            elif value["job"] == "FSB LT":
                fsblt[key] = value
            elif value["job"] == "ISB LT":
                isblt[key] = value
            elif value["job"] == "ASB LT":
                asblt[key] = value
            else:
                print("ERROR: Job Position Not Recognized For:" + value["first"] + " " + value["second"] + " " + value["id"])
    rank = 0
    rankedlst = []
    #Assign rank based on the priority
    for key, value in fsbptl.items():
        rank += 1
        value["overtimerank"] = rank
        rankedlst.append(fsbptl[key])
    for key, value in isbdet.items():
        rank += 1
        value["overtimerank"] = rank
        rankedlst.append(isbdet[key])
    for key, value in asbptl.items():
        rank += 1
        value["overtimerank"] = rank
        rankedlst.append(asbptl[key])
    for key, value in fsbsgt.items():
        rank += 1
        value["overtimerank"] = rank
        rankedlst.append(fsbsgt[key])
    for key, value in isbsgt.items():
        rank += 1
        value["overtimerank"] = rank
        rankedlst.append(isbsgt[key])
    for key, value in asbsgt.items():
        rank += 1
        value["overtimerank"] = rank
        rankedlst.append(asbsgt[key])
    for key, value in fsblt.items():
        rank += 1
        value["overtimerank"] = rank
        rankedlst.append(fsblt[key])
    for key, value in isblt.items():
        rank += 1
        value["overtimerank"] = rank
        rankedlst.append(isblt[key])
    for key, value in asblt.items():
        rank += 1
        value["overtimerank"] = rank
        rankedlst.append(asblt[key])
    return rankedlst
    
#Change the preferred hours for 8 and 4 hour overtime blocks for a given employee id 
def changehours(id, eighthour, fourhour):
    tempfile = NamedTemporaryFile(mode="w", delete=False, newline = "")
    with open (fname, "r") as csvfile, tempfile:
        reader = DictReader(csvfile, fieldnames=fields)
        writer = DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            if row["id"] == id:
                row["8hours"], row["4hours"] = eighthour, fourhour
            writer.writerow(row)
    shutil.move(tempfile.name, fname)
    
#Change the previous position for a given employee id
def changeprevposition(id, prevpos):
    tempfile = NamedTemporaryFile(mode="w", delete=False, newline="")
    with open(fname, "r") as csvfile, tempfile:
        reader = DictReader(csvfile, fieldnames=fields)
        writer = DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            if row["id"] == id:
                row["previousposition"] = prevpos               
            writer.writerow(row)
    shutil.move(tempfile.name, fname)

#Shift row to bottom of csv to reset their rank priority     
def shiftlast(id):
    tempfile = NamedTemporaryFile(mode="w", delete=False, newline="")
    lastrow = {}
    with open(fname, "r") as csvfile, tempfile:
        reader = DictReader(csvfile, fieldnames=fields)
        writer = DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            if row["id"] != id:
                writer.writerow(row)
            else:
                lastrow = row
        if bool(lastrow) == True:
            writer.writerow(lastrow)
    shutil.move(tempfile.name, fname)       

#Move row to its previous position in the csv file
def shiftprevious(prevrow):
    tempfile = NamedTemporaryFile(mode="w", delete=False, newline="")
    count = 0
    if prevrow["previousposition"] == "":
        print("Error: Employee has not been assigned a previous position")
    with open(fname, "r") as csvfile, tempfile:
        reader = DictReader(csvfile, fieldnames=fields)
        writer = DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            count += 1
            if row["id"] != prevrow["id"]:
                if count == int(prevrow["previousposition"]):
                    writer.writerow(prevrow)
                writer.writerow(row)
    shutil.move(tempfile.name, fname)

#Confirm employee up for overtime
def confirmovertime(id):
    position = 0
    tempfile = NamedTemporaryFile(mode="w", delete=False, newline="")
    with open(fname, "r") as csvfile, tempfile:
        reader = DictReader(csvfile, fieldnames=fields)
        writer = DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            position += 1
            if row["id"] == id:
                row["overtimerank"] = "" 
                row["8hours"] = "" 
                row["4hours"] = ""
                row["previousposition"] = str(position)
            writer.writerow(row)
    shutil.move(tempfile.name, fname)
    shiftlast(id)
    
#Cancel overtime for a employee who has been signed up    
def cancelovertime(id):
    dictall = viewall()
    employee = dictall[id]
    shiftprevious(employee)

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
    

#Initialize gui application
def main():  
    #init wx app
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()
    
if __name__ == "__main__":
    main()
    
