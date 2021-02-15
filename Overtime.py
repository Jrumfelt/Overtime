"""
File: Overtime.py
Author: Joseph Rumfelt
Email: jrumfelt1213@gmail.com
Phone: (518)414-1483
Purpose: Determine Overtime position priority for Schenectady PD
"""
from os import remove
import sys
from csv import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import shutil
from PyQt5.QtCore import Qt
from tempfile import NamedTemporaryFile

fname = "Names.csv"
fields = ["id", "last","first","job","8hours","4hours","hiredreason","previousposition"]
unranked = []
unrankedids = []
rankedlst = []

"""
Opens csv file in append mode and adds a new employee using file and writer object
"""
def newemployee(id, last, first, position):
    toAppend = [id, last, first, position, "", "", "", ""]
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
                        "first" : line[1], 
                        "last" : line[2],
                        "job" : line[3],
                        "8hours" : line[4],
                        "4hours" : line[5],
                        "hiredreason": line[6],
                        "previousposition": line[7]
                        }
            dictall[line[0]] = dicttemp
        f_object.close()
    return dictall

"""
Takes a list of employee IDs and calculates their overtime priority rank based on who is higher in Names.csv and job position.
Appends rankedlst
"""
def rank(ids):
    #dictionaries of all the positions
    fsbptl = []
    fsbsgt = []
    fsblt = []
    isbdet = []
    isbsgt = []
    isblt = []
    asbptl = []
    asbsgt = []
    asblt = []
    dictall = viewall()
    #Place in the correct dictionary if it is one of the given ids
    for key, value in dictall.items():
        if key in ids:
            templst = []
            if value["job"] == "FSB PTL":
                for v2 in value.values():
                    templst.append(v2)
                fsbptl.append(templst)
            elif value["job"] == "ISB DET":
                for v2 in value.values():
                    templst.append(v2)
                isbdet.append(templst)
            elif value["job"] == "ASB PTL":
                for v2 in value.values():
                    templst.append(v2)
                asbptl.append(templst)
            elif value["job"] == "FSB SGT":
                for v2 in value.values():
                    templst.append(v2)
                fsbsgt.append(templst)
            elif value["job"] == "ISB SGT":
                for v2 in value.values():
                    templst.append(v2)
                isbsgt.append(templst)
            elif value["job"] == "ASB SGT":
                for v2 in value.values():
                    templst.append(v2)
                asbsgt.append(templst)
            elif value["job"] == "FSB LT":
                for v2 in value.values():
                    templst.append(v2)
                fsblt.append(templst)
            elif value["job"] == "ISB LT":
                for v2 in value.values():
                    templst.append(v2)
                isblt.append(templst)
            elif value["job"] == "ASB LT":
                for v2 in value.values():
                    templst.append(v2)
                asblt.append(templst)
            else:
                print("ERROR: Job Position Not Recognized For:" + value["first"] + " " + value["second"] + " " + value["id"])
    rank = 0
    #Assign rank based on the priority
    for i in fsbptl:
        rank += 1
        i[5] = rank
        rankedlst.append(i)
    for i in isbdet:
        rank += 1
        i[5] = rank
        rankedlst.append(i)
    for i in asbptl:
        rank += 1
        i[5] = rank
        rankedlst.append(i)
    for i in fsbsgt:
        rank += 1
        i[5] = rank
        rankedlst.append(i)
    for i in isbsgt:
        rank += 1
        i[5] = rank
        rankedlst.append(i)
    for i in asbsgt:
        rank += 1
        i[5] = rank
        rankedlst.append(i)
    for i in fsblt:
        rank += 1
        i[5] = rank
        rankedlst.append(i)
    for i in isblt:
        rank += 1
        i[5] = rank
        rankedlst.append(i)
    for i in asblt:
        rank += 1
        i[5] = rank
        rankedlst.append(i)

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
    shifted = False
    if prevrow["previousposition"] == "":
        return False
    prevrow["assigned"] = "No"
    with open(fname, "r") as csvfile, tempfile:
        reader = DictReader(csvfile, fieldnames=fields)
        writer = DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            count += 1
            if shifted == False:
                if row["id"] != prevrow["id"]:
                    if row["assigned"] == "Yes":
                        writer.writerow(prevrow)
                        shifted = True
                    elif int(row["previousposition"]) > int(prevrow["previousposition"]):
                        writer.writerow(prevrow)
                        shifted = True
                    writer.writerow(row)
                else:
                    writer.writerow(prevrow)
            else:
                if row["id"] != prevrow["id"]:
                    writer.writerow(row)
    shutil.move(tempfile.name, fname)
    return True
    
"""
Confirm employee up for overtime
"""
def confirmovertime(id):
    tempfile = NamedTemporaryFile(mode="w", delete=False, newline="")
    with open(fname, "r") as csvfile, tempfile:
        reader = DictReader(csvfile, fieldnames=fields)
        writer = DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            if row["id"] == id:
                row["assigned"] = "Yes" 
                row["8hours"] = "" 
                row["4hours"] = ""
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
Table of employees currently assigned overtime
"""
class AssignedTable(QTableWidget):
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
        assignedlst = []
        with open(fname, "r", newline="") as f_object:
            csvfile = DictReader(f_object, fieldnames=fields)
            for row in csvfile:
                if row["assigned"] == "Yes":
                    id = row["id"]
                    name = row["name"]
                    newrow = [id, name, "Yes"]
                    assignedlst.append(newrow)
        self.setRowCount(0)
        self.setColumnCount(3)
        column = 0
        for row_data in assignedlst:
            row = self.rowCount()
            self.insertRow(row)
            for col_data in row_data:
                item = QTableWidgetItem(col_data)
                self.setItem(row, column, item)
                column +=1
            column = 0

"""
Table of employees signed up for overtime and ranked
"""
class RankedTable(QTableWidget):
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
        rank(unrankedids)
        self.check_change = False
        self.setRowCount(0)
        self.setColumnCount(5)
        column = 0
        for row_data in rankedlst:
            row = self.rowCount()
            self.insertRow(row)
            for col_data in row_data:
                item = QTableWidgetItem(col_data)
                self.setItem(row, column, item)
                column += 1
            column = 0

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
Window with table of ranked employees and form allowing user to assign employees for overtime
"""
class AssignOvertime(QMainWindow):
    def __init__(self):
        super().__init__()
       
        self.setWindowTitle("Overtime Ranks") 
        self.setWindowIcon(QtGui.QIcon("Icon"))
        self.resize(550, 400)
       
        #Create menu bar
        assignbar = self.menuBar()
       
        #Create actions for menu buttons
        assign_action = QAction("Assign Overtime", self)
        close_action = QAction("Close", self)
       
        #Add menu buttons to menu bar
        assignbar.addAction(assign_action)
        assignbar.addAction(close_action)
       
        #Connect menu buttons to functions
        assign_action.triggered.connect(self.assign_triggered)
        close_action.triggered.connect(self.close_triggered)
       
        #set up table
        self.form_widget = RankedTable(10, 10)
        self.setCentralWidget(self.form_widget)
        self.form_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
       
        headers = ["ID", "Name", "Position", "8 Hour", "4 Hour"]
        self.form_widget.setHorizontalHeaderLabels(headers)
       
        self.form_widget.read_list()
    
    def getUID(self):
        uid, okPressed = QInputDialog.getText(self, "Get ID","Employee ID", QLineEdit.Normal, "")
        if okPressed and uid != "":
            return uid
        return None
    
    def assign_triggered(self):
        uid = self.getUID()
        while uid not in unrankedids and uid:
            errdlg = QErrorMessage()
            errdlg.setWindowTitle("ERROR")
            errdlg.showMessage("ERROR: INVALID EMPLOYEE ID---Please ensure the employee ID is correct and that the employee has been signed up")
            errdlg.exec_()
            uid = self.getUID()
        msgBox = QMessageBox()
        msgBox.setText("Confirm Employee Information Is Correct\n____________________________________________\n\nEmployee ID:    " + uid)
        msgBox.setWindowIcon(QtGui.QIcon("Icon"))
        msgBox.setWindowTitle("Confirmation")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        confirm = msgBox.exec_()
        if confirm == QMessageBox.Ok:
            for i in unranked:
                if i[0] == uid:
                    unranked.remove(i)
                    unrankedids.remove(uid)
            for i in rankedlst:
                if i[0] == uid:
                    rankedlst.remove(i)
            confirmovertime(uid)
        self.form_widget.read_list()
    
    def close_triggered(self):
        self.close()
                   
"""
Window with table of signed up employees and form allowing user to add employees to table
""" 
class SignUp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Overtime Sign Up")
        self.setWindowIcon(QtGui.QIcon("Icon"))
        self.resize(450, 400)
        
        #create menu bar
        assignbar = self.menuBar()
        
        #Create actions for menu buttons
        add_action = QAction("Add Employee", self)
        calc_action = QAction("Calculate Overtime", self)
        delete_action = QAction("Withdraw Employee", self)
        close_action = QAction("Close", self)
        
        #Add menu buttons to menu bar
        assignbar.addAction(add_action)
        assignbar.addAction(calc_action)
        assignbar.addAction(delete_action)
        assignbar.addAction(close_action)
        
        #Connect menu buttons to functions
        add_action.triggered.connect(self.add_triggered)
        calc_action.triggered.connect(self.calc_triggered)
        delete_action.triggered.connect(self.delete_triggered)
        close_action.triggered.connect(self.close_triggered)
        
        #set up table
        self.form_widget = UnrankedTable(3,3)
        self.setCentralWidget(self.form_widget)
        self.form_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        headers = ["ID", "8 Hour", "4 Hour"]
        self.form_widget.setHorizontalHeaderLabels(headers)
        
        self.form_widget.read_list()
        
    def getUID(self):
        uid, okPressed = QInputDialog.getText(self, "Get ID","Employee ID", QLineEdit.Normal, "")
        if okPressed and uid != "":
            return uid
        return None
    
    def getEightBlock(self):
        eightblocks = ("0-8", "8-16", "16-24")
        eightblock, okPressed = QInputDialog.getItem(self, "Get Eight Hour Block", "Eight Hour Block", eightblocks, 0, False)
        if okPressed and eightblock:
            return eightblock
        return None           
    
    def getFourBlock(self):
        fourblocks = ("N/A","0-4","4-8","8-12","12-4","16-20","20-24","0-8","8-16","16-24")    #Could change so that it only shows whats relavant to the eight hour blocks
        fourblock, okPressed = QInputDialog.getItem(self, "Get Four Hour Block", "Four Hour Block", fourblocks, 0, False)
        if okPressed and fourblock:
            return fourblock
        else:
            return None

    #Methods for when you press menu button
    """
    Add user to list and update form_widget table
    """
    def add_triggered(self):
        uid = self.getUID()
        dictall = viewall()
        while uid not in dictall and uid:
            errdlg = QErrorMessage()
            errdlg.setWindowTitle("ERROR")
            errdlg.showMessage("ERROR: INVALID EMPLOYEE ID---Please ensure the employee ID is correct and that the employee has been added")
            errdlg.exec_()
            uid = self.getUID()
        while uid and uid in unrankedids:
            errdlg = QErrorMessage()
            errdlg.setWindowTitle("ERROR")
            errdlg.showMessage("ERROR: INVALID EMPLOYEE ID---Please ensure the employee ID has not already been signed up or assigned overtime")
            errdlg.exec_()
            uid = self.getUID()
        if uid:
            eightblock = self.getEightBlock()
            if eightblock:
                fourblock = self.getFourBlock()
                if fourblock:
                    #Confirmation Window
                    msgBox = QMessageBox()
                    msgBox.setText("Confirm Employee Information Is Correct\n____________________________________________\n\nEmployee ID:    " + uid + \
                        "\nEight Hour Block:    " + eightblock + "\nFour Hour Block:    " + fourblock)
                    msgBox.setWindowIcon(QtGui.QIcon("Icon"))
                    msgBox.setWindowTitle("Confirmation")
                    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    
                    confirm = msgBox.exec_()
                    if confirm == QMessageBox.Ok:
                        unrankedids.append(uid)
                        unranked.append([uid, eightblock, fourblock])
                        changehours(uid, eightblock, fourblock)           
        self.form_widget.read_list()
    
    """
    Calculate rank order with rank() and display new window where the user can assign employees to overtime
    """
    def calc_triggered(self):
        if len(unranked) >= 1:
            assign.form_widget.read_list()
            assign.show()
        else:
            errdlg = QErrorMessage()
            errdlg.setWindowTitle("ERROR")
            errdlg.showMessage("ERROR: NOT ENOUGH SIGNED UP---Please ensure there are 2 or more employees signed up for overtime")
            errdlg.exec_()
    
    """
    Remove employee from signed up list
    """
    def delete_triggered(self):
        if len(unranked) > 0:
            uid = self.getUID()
            while uid and uid not in unrankedids:
                errdlg = QErrorMessage()
                errdlg.setWindowTitle("ERROR")
                errdlg.showMessage("ERROR: INVALID EMPLOYEE ID---Please ensure the employee ID is correct and that the employee has been signed up")
                errdlg.exec_()
                uid = self.getUID()
            for i in unranked:
                if i[0] == uid:
                    unranked.remove(i)
                    unrankedids.remove(uid)
            self.form_widget.read_list()
        else:
            errdlg = QErrorMessage()
            errdlg.setWindowTitle("ERROR")
            errdlg.showMessage("ERROR: NO EMPLOYEES SIGNED UP")
            errdlg.exec_()
        
    """
    Close window
    """
    def close_triggered(self):
        self.close()
               
"""
First window with list of all employees and menu bar with buttons to calculate overtime rank, cancel overtime, add new employe, and quit application
"""     
class HomeWindow(QMainWindow):
    def __init__(self):
        super().__init__() 
            
        self.setWindowTitle("Overtime Priority")
        self.setWindowIcon(QtGui.QIcon("Icon"))
        self.resize(500, 400)
        
        #create menu bar
        bar = self.menuBar()
        
        #Create actions for menu buttons
        rank_action = QAction("Schedule Overtime", self)    
        view_action = QAction("View Assigned", self)
        cancel_action = QAction("Cancel Overtime", self)
        newemp_action = QAction("Add New Employee", self)
        quit_action = QAction("Quit", self)
        
        #Add menu buttons to menu bar
        bar.addAction(rank_action)
        bar.addAction(view_action)
        bar.addAction(cancel_action)
        bar.addAction(newemp_action)
        bar.addAction(quit_action)
        
        #Connect menu buttons to functions
        quit_action.triggered.connect(self.quit_trigger)
        view_action.triggered.connect(self.view_triggered)
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
                if success == False:
                    msgBox = QMessageBox()
                    msgBox.setText("Error: Employee overtime could not be cancelled.\nPlease check if employee information is correct and if they were signed up for overtime.")
                    msgBox.setWindowIcon(QtGui.QIcon("Icon"))
                    msgBox.setWindowTitle("Error")
                    msgBox.setStandardButtons(QMessageBox.Ok)
                    msgBox.exec_()
                    
    """
    View table of employees currently assigned to overtime
    """                    
    def view_triggered(self):
        return False

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
    app.setStyle('Fusion')
    home = HomeWindow()
    signup = SignUp()
    assign = AssignOvertime()
    sys.exit(app.exec_())
    
