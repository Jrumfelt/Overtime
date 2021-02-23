"""
File: Overtime.py
Author: Joseph Rumfelt
Email: jrumfelt1213@gmail.com
Phone: (518)414-1483
Purpose: Determine Overtime position priority for Schenectady PD
"""
import sys
from csv import *
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import shutil
from PyQt5.QtCore import Qt
from tempfile import NamedTemporaryFile

fname = "Names.csv"
editfname = "EditLog.txt"
logfname = "HireLog.txt"
fields = ["id", "last","first","job","hired","hiredesc","previousposition"]
unranked = []
unrankedids = []
rankedlst = []

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
                        "first" : line[1], 
                        "last" : line[2],
                        "job" : line[3],
                        "hired" : line[4],
                        "hiredreason": line[5],
                        "previousposition": line[6]
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
    rank = 0
    #Assign rank based on the priority
    for i in fsbptl:
        rank += 1
        i[5] = rank
        if i not in rankedlst:
            rankedlst.append(i)
    for i in isbdet:
        rank += 1
        i[5] = rank
        if i not in rankedlst:
            rankedlst.append(i)
    for i in asbptl:
        rank += 1
        i[5] = rank
        if i not in rankedlst:
            rankedlst.append(i)
    for i in fsbsgt:
        rank += 1
        i[5] = rank
        if i not in rankedlst:
            rankedlst.append(i)
    for i in isbsgt:
        rank += 1
        i[5] = rank
        if i not in rankedlst:
            rankedlst.append(i)
    for i in asbsgt:
        rank += 1
        i[5] = rank
        if i not in rankedlst:
            rankedlst.append(i)
    for i in fsblt:
        rank += 1
        i[5] = rank
        if i not in rankedlst:
            rankedlst.append(i)
    for i in isblt:
        rank += 1
        i[5] = rank
        if i not in rankedlst:
            rankedlst.append(i)
    for i in asblt:
        rank += 1
        i[5] = rank
        if i not in rankedlst:
            rankedlst.append(i)

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
    with open(fname, "r") as csvfile, tempfile:
        reader = DictReader(csvfile, fieldnames=fields)
        writer = DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            if row["id"] == id:
                row["hired"] = "Yes" 
                row["8hours"] = "" 
                row["4hours"] = ""
                row["hiredesc"] = desc
            writer.writerow(row)
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
        rank(unrankedids)
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
        self.setColumnCount(5)
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
        self.setWindowIcon(QtGui.QIcon("Icon"))
        self.resize(800, 600)
        
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
        
        self.edit.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.hire.setLineWrapMode(QPlainTextEdit.NoWrap)
          
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
class EditFile(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Overtime Ranks") 
        self.setWindowIcon(QtGui.QIcon("Icon"))
        self.resize(550, 400)
        
        #Create Menu Bar
        bar = self.menuBar()
        
        #Create Actions
        up_action = QAction("Move Up", self)
        down_action = QAction("Move Down", self)
        submit_action = QAction("Submit Edit", self)
        
        #Add actions to bar
        bar.addAction(up_action)
        bar.addAction(down_action)
        bar.addAction(submit_action)
        
        #Connect actions to functions
        up_action.triggered.connect(self.up_triggered)
        down_action.triggered.connect(self.down_triggered)
        submit_action.triggered.connect(self.submit_triggered)
        
        #Set up table
        self.table_widget = EmployeeTable(10, 10)
        self.setCentralWidget(self.table_widget)
        
        headers = ["ID", "Last", "First", "Job", "Hired", "Hired Description", "Previous Position"]
        self.table_widget.setHorizontalHeaderLabels(headers)
        
        self.table_widget.open_sheet()
        
         
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
       
        headers = ["ID", "Last", "First", "Position", "8 Hour", "4 Hour"]
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
        return None
    
    def getDesc(self):
        desc, okPressed = QInputDialog.getText(self, "Get Hire Description","Hire Description", QLineEdit.Normal, "")
        if okPressed and desc != "":
            return desc
        return None
    
    """
    Hire user specified employee
    """
    def hire_triggered(self):
        uid = self.getUID()
        while uid not in unrankedids and uid:
            errdlg = QErrorMessage()
            errdlg.setWindowTitle("ERROR")
            errdlg.showMessage("ERROR: INVALID EMPLOYEE ID---Please ensure the employee ID is correct and that the employee has been signed up")
            errdlg.exec_()
            uid = self.getUID()
        desc = self.getDesc()
        msgBox = QMessageBox()
        msgBox.setText("Confirm Employee Information Is Correct\n____________________________________________\n\nEmployee ID:    " + uid + "\nDescription:    " + desc)
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
            confirmovertime(uid, desc)
        self.table_widget.read_list()
    
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
        self.table_widget = UnrankedTable(3,3)
        self.setCentralWidget(self.table_widget)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        headers = ["ID", "Last","First","8 Hour", "4 Hour"]
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
    Add user to list and update table_widget table
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
        self.setWindowIcon(QtGui.QIcon("Icon"))
        self.resize(800, 600)
        
        #create menu bar
        bar = self.menuBar()
        
        #Create actions for menu buttons
        rank_action = QAction("Schedule Overtime", self)    
        newemp_action = QAction("Add New Employee", self)
        edit_action = QAction("Editable", self)
        submit_action = QAction("Submit Edit", self)
        quit_action = QAction("Quit", self)
        reset_action = QAction("Reset", self)
        view_action = QAction("View Logs", self)
        
        #Add menu buttons to menu bar
        bar.addAction(rank_action)
        
        #Create edit root menu
        edit = bar.addMenu("Edit")
        
        bar.addAction(reset_action)
        bar.addAction(view_action)
        bar.addAction(quit_action)
        edit.addAction(edit_action)
        edit.addAction(newemp_action)
        edit.addAction(submit_action)
        
        #Connect menu buttons to functions
        quit_action.triggered.connect(self.quit_trigger)
        rank_action.triggered.connect(self.rank_triggered)
        newemp_action.triggered.connect(self.newemp_triggered)
        edit_action.triggered.connect(self.edit_triggered)
        submit_action.triggered.connect(self.submit_triggered)
        reset_action.triggered.connect(self.reset_triggered)
        view_action.triggered.connect(self.view_triggered)
        
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
        palette = QtGui.QPalette()
        if not self.editable:
            self.editable = True
            self.table_widget.verticalHeader().setSectionsMovable(True)
            self.table_widget.verticalHeader().setDragEnabled(True)
            self.table_widget.verticalHeader().setDragDropMode(QAbstractItemView.InternalMove)
            self.table_widget.setEditTriggers(QAbstractItemView.DoubleClicked)
            palette.setColor(QtGui.QPalette.Base, QtGui.QColor("#72889E"))
            palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor("#9E7272"))
            app.setPalette(palette)
        else:
            self.editable = False
            self.table_widget.verticalHeader().setSectionsMovable(False)
            self.table_widget.verticalHeader().setDragEnabled(False)
            self.table_widget.verticalHeader().setDragDropMode(QAbstractItemView.InternalMove)
            self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.table_widget.open_sheet()
            palette.setColor(QtGui.QPalette.Base, QtGui.QColor("#FFFFFF"))
            palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor("#E0E0E0"))
            app.setPalette(palette)

    """
    Save edit to Names.csv and add description to EditLog.txt
    """
    def submit_triggered(self):
        desc = self.getDesc()
        msgBox = QMessageBox()
        msgBox.setText("Confirm edit")
        msgBox.setWindowIcon(QtGui.QIcon("Icon"))
        msgBox.setWindowTitle("Confirmation")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        confirm = msgBox.exec_()
        if confirm == QMessageBox.Ok:
            with open(editfname, "a", newline="") as f:
                f.write(desc + "\n\n")
            rows = self.table_widget.getRows()
            with open(fname, "w", newline="") as f:
                w = writer(f)
                w.writerows(rows)
                
        self.editable = False
        self.table_widget.verticalHeader().setSectionsMovable(False)
        self.table_widget.verticalHeader().setDragEnabled(False)
        self.table_widget.verticalHeader().setDragDropMode(QAbstractItemView.InternalMove)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.open_sheet()
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor("#FFFFFF"))
        palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor("#E0E0E0"))
        app.setPalette(palette)        
        
    """
    When new employee button is clicked prompt the user to enter the id, name, and position of employee
    On user confirmation that the information is correct add to Names.csv using newemployee() function
    """
    def newemp_triggered(self):
        uid = self.getUID()
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
                        msgBox.setWindowIcon(QtGui.QIcon("Icon"))
                        msgBox.setWindowTitle("Confirmation")
                        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                            
                        confirm = msgBox.exec_()
                        if confirm == QMessageBox.Ok:
                            all = viewall()
                            if uid not in all:
                                newemployee(uid, lastname, firstname, position)
                            else:
                                errdlg = QErrorMessage()
                                errdlg.setWindowTitle("ERROR")
                                errdlg.showMessage("ERROR: USER WITH ID: " + uid + " HAS ALREADY BEEN SIGNED UP")
                                errdlg.exec_()
        self.table_widget.open_sheet()
        
    """
    Clear Hired, Hired Description, and Previous Position from Names.csv
    """ 
    def reset_triggered(self):
            msgBox = QMessageBox()
            msgBox.setText("Confirm Rank Reset")
            msgBox.setWindowIcon(QtGui.QIcon("Icon"))
            msgBox.setWindowTitle("Confirmation")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            confirm = msgBox.exec_()
            if confirm == QMessageBox.Ok:
                resetrank()   
                self.table_widget.open_sheet()            
                
    """
    Methods for getting employee information
    """
    def getUID(self):
        uid, okPressed = QInputDialog.getText(self, "Get ID","Employee ID", QLineEdit.Normal, "")
        if okPressed and uid != "":
            return uid
        return None

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
        positions = ("FSB PTL", "FSB SGT", "FSB LT", "ISB PTL", "ISB SGT", "ISB LT", "ASB PTL", "ASB SGT", "ASB LT")
        position, okPressed = QInputDialog.getItem(self, "Get Position", "Employee Position", positions, 0, False)
        if okPressed and position:
            return position
        else:
            return None   
  
    def getDesc(self):
        desc, okPressed = QInputDialog.getText(self, "Get Reason","Reason and Description of Edit", QLineEdit.Normal, "")
        if okPressed and desc != "":
            return desc
        else:
            now = datetime.now()
            now_str = now.strftime("%d/%m/%Y %H:%M:%S")
            return "None Provided: " + now_str
              
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
    
    sys.exit(app.exec_())

