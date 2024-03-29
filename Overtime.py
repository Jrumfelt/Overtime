"""
File: Overtime.py
Author: Joseph Rumfelt
Email: jrumfelt1213@gmail.com
Phone: (518)414-1483
Purpose: Determine Overtime position priority for Schenectady PD
"""
from functools import cmp_to_key
import sys
from csv import *
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import shutil
from PyQt5.QtCore import Qt
from tempfile import NamedTemporaryFile
import webbrowser
import random

fname = "Files/Names.csv"
editfname = "Files/EditLog.txt"
logfname = "Files/HireLog.txt"
bkname = "Backup/Names.csv"
bkedit = "Backup/EditLog.txt"
bklog = "Backup/HireLog.txt"
icon = "Images/Icon.jpg"
fields = ["id", "last","first","job","hired","hiredesc","previousposition"]
jobs = ["FSB PTL", "ISB DET", "ASB PTL", "FSB SGT", "Non-FSB SGT", "FSB LT", "Non-FSB LT"]
unranked = []
unrankedids = []

"""
Opens csv file in append mode and adds a new employee using file and writer object
"""
def newemployee(id, last, first, position):
    toAppend = [id, last, first, position,"", "", ""]
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
                break
            dicttemp = {
                        "id" : line[0],
                        "last" : line[1], 
                        "first" : line[2],
                        "job" : line[3],
                        "hired" : line[4],
                        "hiredreason": line[5],
                        "previousposition": line[6]
                        }
            dictall[line[0]] = dicttemp
        f_object.close()
    return dictall

"""
Custom comparator to sort list by job and position
"""
def job_comparator(lhs, rhs):
    #Compare based on job
    comp = (jobs.index(lhs[3]) > jobs.index(rhs[3])) - (jobs.index(lhs[3]) < jobs.index(rhs[3]))
    if comp == 0:
        #Compare based on list position if job is the same
        comp = (lhs[6] > rhs[6]) - (lhs[6] < rhs[6])
    return comp
"""
Takes a list of employee IDs and calculates their overtime priority rank based on who is higher in Names.csv and job position.
Appends rankedlst
"""
def rank(unranked):
    if len(unranked) > 1:
        rankedlst = sorted(unranked, key = cmp_to_key(job_comparator))
    else:
        rankedlst = unranked
    return rankedlst

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
Confirm employee up for overtime
"""
def confirmovertime(id, desc):
    tempfile = NamedTemporaryFile(mode="w", delete=False, newline="")
    count = 1
    with open(fname, "r") as csvfile, tempfile:
        reader = DictReader(csvfile, fieldnames=fields)
        writer = DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            if row["id"] == id:
                row["hired"] = "Yes" 
                row["hiredesc"] = desc
                row["previousposition"] = count
            writer.writerow(row)
            count += 1
    shutil.move(tempfile.name, fname)
    shiftlast(id)
    
"""
Reset the Hired, Hired Description, and Previous Position from Names.csv
"""
def resetrank():
    tempfile = NamedTemporaryFile(mode="w", delete=False, newline="")
    with open(fname, "r") as csvfile, tempfile:
        reader = DictReader(csvfile, fieldnames=fields)
        writer = DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            if row["hired"] == "Yes":
                log(row)
            row["hired"], row["hiredesc"], row["previousposition"] = "","",""
            writer.writerow(row)    
    shutil.move(tempfile.name, fname)
    #Backup files by copying them to backup dir
    shutil.copyfile(fname, bkname)
    shutil.copyfile(editfname, bkedit)
    shutil.copyfile(logfname, bklog)
    
    
        
"""
Log the hire information to HireLog.txt from a given row
"""
def log(row):
    logstr = row["id"] + ", " + row["last"] + ", " +  row["first"] + " : " + row["hiredesc"] + "\n\n"
    with open(logfname, "a", newline="") as f_object:
        f_object.write(logstr)
        
"""
GUI classes and methods
"""

"""
Table of employees currently hired for overtime
"""
class HiredTable(QTableWidget):
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
        hiredlst = []
        with open(fname, "r", newline="") as f_object:
            csvfile = DictReader(f_object, fieldnames=fields)
            for row in csvfile:
                if row["hired"] == "Yes":
                    id = row["id"]
                    name = row["name"]
                    newrow = [id, name, "Yes"]
                    hiredlst.append(newrow)
        self.setRowCount(0)
        self.setColumnCount(3)
        column = 0
        for row_data in hiredlst:
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
        rankedlst = rank(unranked)
        self.check_change = False
        self.setRowCount(0)
        self.setColumnCount(6)
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
        self.setColumnCount(6)
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
Table of employees with all information
"""     
class EmployeeTable(QTableWidget):
    def __init__(self, r, c):
        super().__init__(r, c)
        self.check_change = True
        self.init_ui()
        
    def init_ui(self):
        self.show()
    
    def open_sheet(self):
        self.check_change = False
        with open(fname, "r" , newline="") as f_object:
            self.setRowCount(0)
            self.setColumnCount(7)
            my_file = reader(f_object)
            for row_data in my_file:
                row = self.rowCount()
                self.insertRow(row)
                for column, stuff in enumerate(row_data):
                    item = QTableWidgetItem(stuff)
                    self.setItem(row, column, item)
        self.check_change = True 
    
    def getRows(self):
        rows = []
        for row in range(self.rowCount()):
            row_data = []
            for column in range(self.columnCount()):
                item = self.item(row, column)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            rows.append(row_data)
        return rows
    
"""
Window showing edit and hire logs
"""   
class ViewLogs(QWidget):
    def __init__(self):
        super(ViewLogs, self).__init__()
        
        self.edit = QPlainTextEdit(self)
        self.hire = QPlainTextEdit(self)
        self.editlabel = QLabel(self)
        self.hirelabel = QLabel(self)
        
        self.setWindowTitle("View Logs") 
        self.setWindowIcon(QtGui.QIcon(icon))
        self.resize(900, 700)
        
        self.init_ui()
        
    def init_ui(self):
        outerlayout = QVBoxLayout()
        labellayout = QHBoxLayout()
        loglayout = QHBoxLayout()
        
        labellayout.addWidget(self.editlabel)
        labellayout.addWidget(self.hirelabel)
        
        loglayout.addWidget(self.edit)
        loglayout.addWidget(self.hire)
        
        outerlayout.addLayout(labellayout)
        outerlayout.addLayout(loglayout)
        
        self.setLayout(outerlayout)
        self.setWindowTitle("Logs")
        
        self.edit.setReadOnly(True)
        self.hire.setReadOnly(True)
          
        self.editlabel.setText("Edit Log")
        self.hirelabel.setText("Hire Log")
        
        self.edit.setFont(QtGui.QFont("Times", 10))
        self.hire.setFont(QtGui.QFont("Times", 10))
        self.editlabel.setFont(QtGui.QFont("Arial", 20))
        self.hirelabel.setFont(QtGui.QFont("Arial", 20))
    
        self.init_text()
    
    def init_text(self):
        edit_text = open(editfname).read()
        hire_text = open(logfname).read()
        
        self.edit.setPlainText(edit_text)
        self.hire.setPlainText(hire_text)

"""
Window for editing Names.csv
"""
class EditFile(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Overtime Ranks") 
        self.setWindowIcon(QtGui.QIcon(icon))
        self.resize(1100, 600)
        
        self.UiComponents()

    def UiComponents(self):
        #Table Widget
        self.table_widget = EmployeeTable(10, 10)
        headers = ["ID", "Last", "First", "Job", "Hired", "Hired Description", "Previous Position"]
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_widget.open_sheet()

        #Button Widgets
        self.delete = QPushButton(self)
        self.delete.setText("Delete Row")
        self.submit = QPushButton(self)
        self.submit.setText("Submit Changes")
        #Movement buttons
        self.upOne = QPushButton(self)
        self.upOne.setText("Move Up 1")
        self.upTen = QPushButton(self)
        self.upTen.setText("Move Up 10")
        self.upFifty = QPushButton(self)
        self.upFifty.setText("Move Up 50")
        self.downOne = QPushButton(self)
        self.downOne.setText("Move Down 1")
        self.downTen = QPushButton(self)
        self.downTen.setText("Move Down 10")
        self.downFifty = QPushButton(self)
        self.downFifty.setText("Move Down 50")

        #layout
        grid = QGridLayout()
        grid2 = QGridLayout()

        grid.addWidget(self.table_widget,0,0)
        grid.addLayout(grid2,0,1)
        grid2.addWidget(self.upOne,0,0)
        grid2.addWidget(self.upTen,0,1)
        grid2.addWidget(self.upFifty,0,2)
        grid2.addWidget(self.downOne,1,0)
        grid2.addWidget(self.downTen,1,1)
        grid2.addWidget(self.downFifty,1,2)
        grid2.addWidget(self.delete,2,0)
        grid2.addWidget(self.submit,2,1)

        self.setLayout(grid)

        #Button Events
        self.upOne.clicked.connect(self.up_triggered)
        self.upTen.clicked.connect(self.upTen_triggered)
        self.upFifty.clicked.connect(self.upFifty_triggered)
        self.downOne.clicked.connect(self.down_triggered)
        self.downTen.clicked.connect(self.downTen_triggered)
        self.downFifty.clicked.connect(self.downFifty_triggered)
        self.submit.clicked.connect(self.submit_triggered)
        self.delete.clicked.connect(self.delete_triggered)
        
    """
    Move Selected Row Up
    """
    def upTen_triggered(self):
        count = 10
        while count > 0:
            self.up_triggered()
            count -= 1

    def upFifty_triggered(self):
        count = 50
        while count > 0:
            self.up_triggered()
            count -= 1

    def up_triggered(self):
        row = self.table_widget.currentRow()
        colcount = self.table_widget.columnCount()
        col = 0
        if row > 0:
            self.table_widget.insertRow(row - 1)
            while col < colcount:
                self.table_widget.setItem(row - 1, col, self.table_widget.takeItem(row + 1, col))
                col += 1
            self.table_widget.removeRow(row + 1)
        self.table_widget.selectRow(row - 1)
                
    """
    Move selected row down
    """
    def downTen_triggered(self):
        count = 10
        while count > 0:
            self.down_triggered()
            count -= 1

    def downFifty_triggered(self):
        count = 50
        while count > 0:
            self.down_triggered()
            count -= 1

    def down_triggered(self):
        row = self.table_widget.currentRow()
        colcount = self.table_widget.columnCount()
        rowcount = self.table_widget.rowCount()
        col = 0
        if row < rowcount - 1:
            self.table_widget.insertRow(row + 2)
            while col < colcount:
                self.table_widget.setItem(row + 2, col, self.table_widget.takeItem(row, col))
                col += 1
            self.table_widget.removeRow(row)
        self.table_widget.selectRow(row + 1)
        
    """
    Delete selected row
    """
    def delete_triggered(self):
        row = self.table_widget.currentRow()
        self.table_widget.removeRow(row)
    
    """
    Save edit to Names.csv and add description to EditLog.txt
    """
    def submit_triggered(self):
        desc = self.getDesc()
        if desc:
            msgBox = QMessageBox()
            msgBox.setText("Confirm edit")
            msgBox.setWindowIcon(QtGui.QIcon(icon))
            msgBox.setWindowTitle("Confirmation")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            
            confirm = msgBox.exec_()
            if confirm == QMessageBox.Ok:
                now = datetime.now()
                nowstr = now.strftime("%m/%d/%Y %H:%M:%S")
                with open(editfname, "a", newline="") as f:
                    f.write(nowstr + " " + desc + "\n\n")
                rows = self.table_widget.getRows()
                with open(fname, "w", newline="") as f:
                    w = writer(f)
                    w.writerows(rows)
        self.table_widget.open_sheet()
                
    """
    Get user input for description of edit
    """
    def getDesc(self):
        desc, okPressed = QInputDialog.getText(self, "Get Reason","Reason and Description of Edit", QLineEdit.Normal, "")
        if okPressed and desc != "":
            return desc
        else:
            return None
            
"""
Window with table of ranked employees and form allowing user to assign employees for overtime
"""
class AssignOvertime(QMainWindow):
    def __init__(self):
        super().__init__()
       
        self.setWindowTitle("Overtime Ranks") 
        self.setWindowIcon(QtGui.QIcon(icon))
        self.resize(650, 400)
       
        #Create menu bar
        assignbar = self.menuBar()
       
        #Create actions for menu buttons
        hire_action = QAction("Hire", self)
        close_action = QAction("Close", self)
       
        #Add menu buttons to menu bar
        assignbar.addAction(hire_action)
        assignbar.addAction(close_action)
       
        #Connect menu buttons to functions
        hire_action.triggered.connect(self.hire_triggered)
        close_action.triggered.connect(self.close_triggered)
       
        #set up table
        self.table_widget = RankedTable(10, 10)
        self.setCentralWidget(self.table_widget)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
       
        headers = ["ID", "Last", "First", "Position", "8 Hour Block", "4 Hour Block"]
        self.table_widget.setHorizontalHeaderLabels(headers)
       
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.read_list()
    
    """
    Methods for user input
    """
    def getUID(self):
        uid, okPressed = QInputDialog.getText(self, "Get ID","Employee ID", QLineEdit.Normal, "")
        if okPressed and uid != "":
            return uid
        else:
            return None
    
    def getDesc(self):
        desc, okPressed = QInputDialog.getText(self, "Get Hire Description","Hire Description", QLineEdit.Normal, "")
        if okPressed and desc != "":
            return desc
        else:
            return None
        
    def getLast(self):
        last, okPressed = QInputDialog.getText(self, "Get Last Name","Employee Last Name", QLineEdit.Normal, "")
        if okPressed and last != "":
            return last
        return None
    
    def getFirst(self, last):
        options = []
        dictall = viewall()
        for value in dictall.values():
            if value["last"].upper() == last.upper():
                options.append(value["first"])
        first, okPressed = QInputDialog.getItem(self, "Get First Name","Employee First Name", options, 0, False)
        if okPressed and first != "":
            return first
        return None
    
    """
    Hire user specified employee
    """
    def hire_triggered(self):
        uid = None
        dictall = viewall()
        last = self.getLast()
        if last:
            first = self.getFirst(last)
            if first:
                for value in dictall.values():
                    if value["last"].upper() == last.upper():
                        if value["first"].upper() == first.upper():
                            print("here")
                            uid = value["id"]
        if not uid:
            errdlg = QErrorMessage()
            errdlg.setWindowTitle("ERROR")
            errdlg.showMessage("ERROR: INVALID EMPLOYEE NAME---Please ensure the name is correct and that the employee has been added")
            errdlg.exec_()
        if uid:
            if uid not in unrankedids and uid:
                errdlg = QErrorMessage()
                errdlg.setWindowTitle("ERROR")
                errdlg.showMessage("ERROR: INVALID EMPLOYEE ID---Please ensure the employee ID is correct and that the employee has been signed up")
                errdlg.exec_()
            else:
                desc = self.getDesc()
                if desc:
                    msgBox = QMessageBox()
                    msgBox.setText("Confirm Employee Information Is Correct\n____________________________________________\n\nEmployee ID:    " + uid + "\nDescription:    " + desc)
                    msgBox.setWindowIcon(QtGui.QIcon(icon))
                    msgBox.setWindowTitle("Confirmation")
                    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    confirm = msgBox.exec_()
                    if confirm == QMessageBox.Ok:
                        for i in unranked:
                            if i[0] == uid:
                                unranked.remove(i)
                                unrankedids.remove(uid)
                        confirmovertime(uid, desc)
        self.table_widget.read_list()
        home.table_widget.open_sheet()
        signup.table_widget.read_list()
        
    
    """
    Close Window
    """
    def close_triggered(self):
        self.close()
                   
"""
Window with table of signed up employees and form allowing user to add employees to table
""" 
class SignUp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Overtime Sign Up")
        self.setWindowIcon(QtGui.QIcon(icon))
        self.resize(650, 400)
        
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
        self.table_widget = UnrankedTable(10,10)
        self.setCentralWidget(self.table_widget)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        headers = ["ID", "Last", "First", "Job", "8 Hour Block", "4 Hour Block"]
        self.table_widget.setHorizontalHeaderLabels(headers)
        
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.read_list()
     
    """
    Methods to get user input
    """   
    def getUID(self):
        uid, okPressed = QInputDialog.getText(self, "Get ID","Employee ID", QLineEdit.Normal, "")
        if okPressed and uid != "":
            return uid
        return None
    
    def getLast(self):
        last, okPressed = QInputDialog.getText(self, "Get Last Name","Employee Last Name", QLineEdit.Normal, "")
        if okPressed and last != "":
            return last
        return None
    
    def getFirst(self, last):
        options = []
        dictall = viewall()
        for value in dictall.values():
            if value["last"].upper() == last.upper():
                options.append(value["first"])
        first, okPressed = QInputDialog.getItem(self, "Get First Name","Employee First Name", options, 0, False)
        if okPressed and first != "":
            return first
        return None
    
    def getEightBlock(self):
        eightblocks = ("0-8", "8-16", "16-24")
        eightblock, okPressed = QInputDialog.getItem(self, "Get Eight Hour Block", "Eight Hour Block", eightblocks, 0, False)
        if okPressed and eightblock:
            return eightblock
        return None          
    
    def getFourBlock(self, eightblock):
        if eightblock == "0-8":
            fourblocks = ("N/A", "0-4", "4-8", "0-8")
        elif eightblock == "8-16":
            fourblocks = ("N/A", "8-12", "12-16", "8-16")
        elif eightblock == "16-24":
            fourblocks = ("N/A", "16-20", "20-24", "16-24")
        fourblock, okPressed = QInputDialog.getItem(self, "Get Four Hour Block", "Four Hour Block", fourblocks, 0, False)
        if okPressed and fourblock:
            return fourblock
        else:
            return None

    #Methods for when you press menu button
    """
    Add user to list and update table_widget table
    """
    def add_triggered(self):
        uid = None
        dictall = viewall()
        last = self.getLast()
        if last:
            first = self.getFirst(last)
            if first:
                for value in dictall.values():
                    if value["last"].upper() == last.upper():
                        if value["first"].upper() == first.upper():
                            uid = value["id"]
        if not uid:
            errdlg = QErrorMessage()
            errdlg.setWindowTitle("ERROR")
            errdlg.showMessage("ERROR: INVALID EMPLOYEE NAME---Please ensure the name is correct and that the employee has been added")
            errdlg.exec_()
        if uid:
            eightblock = self.getEightBlock()
            if eightblock:
                fourblock = self.getFourBlock(eightblock)
                if fourblock:
                    #Confirmation Window
                    msgBox = QMessageBox()
                    msgBox.setText("Confirm Employee Information Is Correct\n____________________________________________\n\nEmployee ID:    " + uid + \
                        "\nEight Hour Block:    " + eightblock + "\nFour Hour Block:    " + fourblock)
                    msgBox.setWindowIcon(QtGui.QIcon(icon))
                    msgBox.setWindowTitle("Confirmation")
                    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    
                    confirm = msgBox.exec_()
                    if confirm == QMessageBox.Ok:
                        pos = list(dictall.keys()).index(uid)
                        last = dictall[uid]["last"]
                        first = dictall[uid]["first"]
                        job = dictall[uid]["job"]
                        unrankedids.append(uid)
                        unranked.append([uid, last, first, job, eightblock, fourblock, pos])
        self.table_widget.read_list()
    
    """
    Calculate rank order with rank() and display new window where the user can assign employees to overtime
    """
    def calc_triggered(self):
        if len(unranked) >= 1:
            assign.table_widget.read_list()
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
            self.table_widget.read_list()
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
First window with list of all employees and menu bar with buttons to calculate overtime rank, cancel overtime, edit, and quit application
"""     
class HomeWindow(QMainWindow):
    def __init__(self):
        super().__init__() 
            
        self.editable = False
        self.setWindowTitle("Overtime Priority")
        self.setWindowIcon(QtGui.QIcon(icon))
        self.resize(800, 600)
        
        #create menu bar
        bar = self.menuBar()
        
        #Create actions for menu buttons
        rank_action = QAction("Schedule Overtime", self)    
        newemp_action = QAction("Add New Employee", self)
        edit_action = QAction("Edit", self)
        quit_action = QAction("Quit", self)
        reset_action = QAction("Reset", self)
        view_action = QAction("View Logs", self)
        help_action = QAction("Help", self)
        
        #Add menu buttons to menu bar
        bar.addAction(rank_action)
        bar.addAction(edit_action)
        bar.addAction(reset_action)
        bar.addAction(view_action)
        bar.addAction(newemp_action)
        bar.addAction(help_action)
        bar.addAction(quit_action)
        
        
        #Connect menu buttons to functions
        quit_action.triggered.connect(self.quit_trigger)
        rank_action.triggered.connect(self.rank_triggered)
        newemp_action.triggered.connect(self.newemp_triggered)
        edit_action.triggered.connect(self.edit_triggered)
        reset_action.triggered.connect(self.reset_triggered)
        view_action.triggered.connect(self.view_triggered)
        help_action.triggered.connect(self.help_triggered)
        
        #set up table
        self.table_widget = EmployeeTable(10, 10)
        self.setCentralWidget(self.table_widget)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            
        headers = ["ID", "Last", "First", "Job", "Hired", "Hired Description", "Previous Position"]
        self.table_widget.setHorizontalHeaderLabels(headers)
            
        self.table_widget.setAlternatingRowColors(True)
        
        self.table_widget.open_sheet()
            
        #show window
        self.show()              
    
    """
    Methods for when you press menu button    
    """
    """
    Quit application
    """
    def quit_trigger(self):
        qApp.quit()
        
    """
    Open Github demo page
    """
    def help_triggered(self):
        webbrowser.open("https://github.com/Jrumfelt/Overtime#demo")
    
    """
    Show signup page
    """
    def rank_triggered(self):
        signup.show()
        
    """
    Show ViewLogs window
    """
    def view_triggered(self):
        view_logs.init_text()
        view_logs.show()
     
    """
    Allow user to edit Names.csv
    """    
    def edit_triggered(self):
        editfile.table_widget.open_sheet()
        editfile.show()     
        
    """
    When new employee button is clicked prompt the user to enter the id, name, and position of employee
    On user confirmation that the information is correct add to Names.csv using newemployee() function
    """
    def newemp_triggered(self):
        uid = str(random.randint(0, 9999))
        all = viewall()
        while uid in all:
            uid = str(random.randint(0,9999))
        if uid:
            lastname = self.getLast()
            if lastname:
                firstname = self.getFirst()
                if firstname:
                    position = self.getPosition()
                    if position:
                        #Create confirmation window
                        msgBox = QMessageBox()
                        msgBox.setText("Confirm Employee Information Is Correct\n____________________________________________\n\nEmployee ID:    " + uid + \
                            "\nEmployee Name:    " + lastname + " " + firstname + "\nEmployee Position:    " + position)
                        msgBox.setWindowIcon(QtGui.QIcon(icon))
                        msgBox.setWindowTitle("Confirmation")
                        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                            
                        confirm = msgBox.exec_()
                        if confirm == QMessageBox.Ok:
                            newemployee(uid, lastname, firstname, position)
                            now = datetime.now()
                            nowstr = now.strftime("%m/%d/%Y %H:%M:%S")
                            desc = "New employee added: " + uid + ", " + lastname + ", " + firstname + ", " + position
                            with open(editfname, "a", newline="") as f:
                                f.write(nowstr + " " + desc + "\n\n")
        self.table_widget.open_sheet()
        
    """
    Clear Hired, Hired Description, and Previous Position from Names.csv
    """ 
    def reset_triggered(self):
            msgBox = QMessageBox()
            msgBox.setText("Confirm Rank Reset")
            msgBox.setWindowIcon(QtGui.QIcon(icon))
            msgBox.setWindowTitle("Confirmation")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            confirm = msgBox.exec_()
            if confirm == QMessageBox.Ok:
                resetrank()   
                self.table_widget.open_sheet()            
                
    """
    Methods for getting employee information
    """
    def getLast(self):
        name, okPressed = QInputDialog.getText(self, "Get Name", "Employee Last Name", QLineEdit.Normal, "")
        if okPressed and name != "":
            return name
        else:
            return None
    
    def getFirst(self):
        name, okPressed = QInputDialog.getText(self, "Get Name", "Employee First Name", QLineEdit.Normal, "")
        if okPressed and name != "":
            return name
        else:
            return None
       
    def getPosition(self):
        positions = ("FSB PTL", "FSB SGT", "FSB LT", "ISB DET", "ISB SGT", "ISB LT", "ASB PTL", "ASB SGT", "ASB LT")
        position, okPressed = QInputDialog.getItem(self, "Get Position", "Employee Position", positions, 0, False)
        if okPressed and position:
            return position
        else:
            return None
              
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setStyle('Fusion')
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor("#FFFFFF"))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor("#E0E0E0"))
    app.setPalette(palette)
    
    home = HomeWindow()
    signup = SignUp()
    assign = AssignOvertime()
    view_logs = ViewLogs()
    editfile = EditFile()
    
    sys.exit(app.exec_())

