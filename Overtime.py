"""
File: Overtime.py
Author: Joseph Rumfelt
Email: jrumfelt1213@gmail.com
Phone: (518)414-1483
Purpose: Determine Overtime position priority for Schenectady PD
"""
from os import close
import sys
from csv import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import shutil
from PyQt5.QtCore import Qt
from tempfile import NamedTemporaryFile

fname = "Names.csv"
fields = ["id", "name", "job", "8hours", "4hours", "overtimerank", "previousposition"]
unranked = []

"""
Opens csv file in append mode and adds a new employee using file and writer object
"""
def newemployee(id, name, position):
    toAppend = [id, name, position, "", "", "", ""]
    with open(fname, "a", newline="") as f_object:
        csv_writer = writer(f_object)
        csv_writer.writerow(toAppend)
        f_object.close()

"""        
Returns a dict of all employees with id as key and the values being a 
dictionary with first name, last name, total overtime, 8hours, 4hours, overtime rank, and previous position in file   
"""
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
                        "8hours" : line[3],
                        "4hours" : line[4],
                        "overtimerank" : line[5],
                        "previousposition": line[6],
                        }
            dictall[line[0]] = dicttemp
        f_object.close()
    return dictall

"""
Takes a list of employee IDs and calculates their overtime priority rank based on who is higher in Names.csv and job position.
Returns a dictionary with the employee information and rank
"""
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

"""    
Change the preferred hours for 8 and 4 hour overtime blocks for a given employee id 
"""
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

"""
Shift row to bottom of csv to reset their rank priority 
"""    
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
         
"""
Move row to its previous position in the csv file
"""
def shiftprevious(prevrow):
    tempfile = NamedTemporaryFile(mode="w", delete=False, newline="")
    count = 0
    if prevrow["previousposition"] == "":
        return False
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
    return True
    
"""
Confirm employee up for overtime
"""
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
    
"""    
Cancel overtime for a employee who has been signed up    
"""
def cancelovertime(id):
    dictall = viewall()
    if id in dictall:
        employee = dictall[id]
        return(shiftprevious(employee))
    else:
        return False

"""
GUI classes and methods
"""

"""
Table of employees signed up for overtime but not ranked
"""
class UnrankedTable(QTableWidget):
    def __init__(self, r, c):
        super().__init__(r, c)
        self.check_change = True
        self.init_ui()
        
    def init_ui(self):
        self.cellChanged.connect(self.c_current)
        self.show()
        
    def c_current(self):
        if self.check_change:
            row = self.currentRow()
            col = self.currentColumn()
            value = self.item(row, col)
            value = value.text()
            
    def read_list(self):
        self.check_change = False
        self.setRowCount(0)
        self.setColumnCount(3)
        column = 0
        for row_data in unranked:
            row = self.rowCount()
            self.insertRow(row)
            for col_data in row_data: 
                item = QTableWidgetItem(col_data)
                self.setItem(row, column, item)
                column += 1
            column = 0
                
"""
Window with table of signed up employees and form allowing user to add employees to table
""" 
class SignUp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Assign Overtime")
        self.setWindowIcon(QtGui.QIcon("Icon"))
        self.resize(450, 400)
        
        #create menu bar
        assignbar = self.menuBar()
        
        #Create actions for menu buttons
        add_action = QAction("Add Employee", self)
        calc_action = QAction("Calculate Overtime", self)
        close_action = QAction("Close", self)
        
        #Add menu buttons to menu bar
        assignbar.addAction(add_action)
        assignbar.addAction(calc_action)
        assignbar.addAction(close_action)
        
        #Connect menu buttons to functions
        add_action.triggered.connect(self.add_triggered)
        calc_action.triggered.connect(self.calc_triggered)
        close_action.triggered.connect(self.close_triggered)
        
        #set up table
        self.form_widget = UnrankedTable(3,3)
        self.setCentralWidget(self.form_widget)
        self.form_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        headers = ["ID", "8 Hour", "4 Hour"]
        self.form_widget.setHorizontalHeaderLabels(headers)
        
        self.form_widget.read_list()
        
    #Methods for when you press menu button
    """
    Add user to list and update form_widget table
    """
    def add_triggered(self):
        return False
    
    """
    Calculate rank order with rank() and display new window where the user can assign employees to overtime
    """
    def calc_triggered(self):
        return False
        
    """
    Close window
    """
    def close_triggered(self):
        self.close()

"""
Table of employees
"""     
class EmployeeTable(QTableWidget):
    def __init__(self, r, c):
        super().__init__(r, c)
        self.check_change = True
        self.init_ui()
        
    def init_ui(self):
        self.cellChanged.connect(self.c_current)
        self.show()
        
    def c_current(self):
        if self.check_change:
            row = self.currentRow()
            col = self.currentColumn()
            value = self.item(row, col)
            value = value.text()
    
    def open_sheet(self):
        self.check_change = False
        fname = "Names.csv"
        with open(fname, "r" , newline="") as f_object:
            self.setRowCount(0)
            self.setColumnCount(3)
            my_file = reader(f_object)
            for row_data in my_file:
                row = self.rowCount()
                self.insertRow(row)
                for column, stuff in enumerate(row_data):
                    item = QTableWidgetItem(stuff)
                    self.setItem(row, column, item)
        self.check_change = True    
               
"""
First window with list of all employees and menu bar with buttons to calculate overtime rank, cancel overtime, add new employe, and quit application
"""     
class HomeWindow(QMainWindow):
    def __init__(self):
        super().__init__() 
            
        self.setWindowTitle("Overtime Priority")
        self.setWindowIcon(QtGui.QIcon("Icon"))
        self.resize(450, 400)
        
        #create menu bar
        bar = self.menuBar()
        
        #Create actions for menu buttons
        rank_action = QAction("Schedule Overtime", self)    
        cancel_action = QAction("Cancel Overtime", self)
        newemp_action = QAction("Add New Employee", self)
        quit_action = QAction("Quit", self)
        
        #Add menu buttons to menu bar
        bar.addAction(rank_action)
        bar.addAction(cancel_action)
        bar.addAction(newemp_action)
        bar.addAction(quit_action)
        
        #Connect menu buttons to functions
        quit_action.triggered.connect(self.quit_trigger)
        rank_action.triggered.connect(self.rank_triggered)
        cancel_action.triggered.connect(self.cancel_triggered)
        newemp_action.triggered.connect(self.newemp_triggered)
        
        #set up table
        self.form_widget = EmployeeTable(10, 10)
        self.setCentralWidget(self.form_widget)
        self.form_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
            
        headers = ["ID", "Name", "Position"]
        self.form_widget.setHorizontalHeaderLabels(headers)
            
        self.form_widget.open_sheet()
            
        #show window
        self.show()              
    
    #Methods for when you press menu button    
    def quit_trigger(self):
        qApp.quit()
    
    def rank_triggered(self):
        signup.show()
        
    #Methods for getting employee information
    def getUID(self):
        uid, okPressed = QInputDialog.getText(self, "Get ID","Employee ID", QLineEdit.Normal, "")
        if okPressed and uid != "":
            return uid
        return None

    def getName(self):
        name, okPressed = QInputDialog.getText(self, "Get Name", "Employee Name", QLineEdit.Normal, "")
        if okPressed and name != "":
            return name
        else:
            return None
        
    def getPosition(self):
        positions = ("FSB PTL", "FSB SGT", "FSB LT", "ISB PTL", "ISB SGT", "ISB LT", "ASB PTL", "ASB SGT", "ASB LT")
        position, okPressed = QInputDialog.getItem(self, "Get Position", "Employee Position", positions, 0, False)
        if okPressed and position:
            return position
        else:
            return None
    
    """
    When cancel overtime button is clicked prompt the user to enter the id of the user to be remove
    Prompt user to confirm and if confirmed prompt if the user would like to select a new user for overtime
    """    
    def cancel_triggered(self):
        uid = self.getUID()
        if uid:
            msgBox = QMessageBox()
            msgBox.setText("Confirm Employee Information Is Correct\n____________________________________________\n\nEmployee ID:    " + uid)
            msgBox.setWindowIcon(QtGui.QIcon("Icon"))
            msgBox.setWindowTitle("Confirmation")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    
            confirm = msgBox.exec_()
            
            if confirm == QMessageBox.Ok:
                success = cancelovertime(uid)
                print(success)
                if success == False:
                    msgBox = QMessageBox()
                    msgBox.setText("Error: Employee overtime could not be cancelled.\nPlease check if employee information is correct and if they were signed up for overtime.")
                    msgBox.setWindowIcon(QtGui.QIcon("Icon"))
                    msgBox.setWindowTitle("Error")
                    msgBox.setStandardButtons(QMessageBox.Ok)
                    msgBox.exec_()
                else:
                    #ask if they want to assign someone new
                    msgBox = QMessageBox()
                    msgBox.setText("Assign New Employee to Overtime?")
                    msgBox.setWindowIcon(QtGui.QIcon("Icon"))
                    msgBox.setWindowTitle("Confirmation")
                    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    
                    confirm = msgBox.exec_()
                    
                    if confirm == QMessageBox.Ok:
                        signup.show()
                        #Change assign to other window

    """
    When new employee button is clicked prompt the user to enter the id, name, and position of employee
    On user confirmation that the information is correct add to Names.csv using newemployee() function
    """
    def newemp_triggered(self):
        uid = self.getUID()
        if uid:
            name = self.getName()
            if name:
                position = self.getPosition()
                if position:
                    #Create confirmation window
                    msgBox = QMessageBox()
                    msgBox.setText("Confirm Employee Information Is Correct\n____________________________________________\n\nEmployee ID:    " + uid + \
                        "\nEmployee Name:    " + name + "\nEmployee Position:    " + position)
                    msgBox.setWindowIcon(QtGui.QIcon("Icon"))
                    msgBox.setWindowTitle("Confirmation")
                    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    
                    confirm = msgBox.exec_()
                    if confirm == QMessageBox.Ok:
                        newemployee(uid, name, position)
        self.form_widget.open_sheet()    
                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    home = HomeWindow()
    signup = SignUp()
    sys.exit(app.exec_())
    
