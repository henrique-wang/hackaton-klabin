""""
This file has all functions responsible for checking and editing informations from databases in offline mode
"""

import pandas as pd
import importlib
employee_class = importlib.import_module("classes.employee_class", ".")
#.load_source("classes", "../classes/employee_class.py")

# Get all employees from database
# Return List<Employee>
def getAllEmployees():
    dataBase = pd.read_csv('employee_db.csv')
    employee_list = []
    for i in range(len(dataBase)):
        employee_name = dataBase["first_name"][i]
        employee_id = dataBase["idemp"][i]
        employee_email = dataBase["email"][i]
        curr_employee = employee_class.Employee(employee_name, employee_email, employee_id)
        employee_list.append(curr_employee)
    return employee_list

# Search for employee using his email
# Receive String userEmail
# Return Employee
def getEmployeePerEmail(userEmail):
    dataBase = pd.read_csv('employee_db.csv')
    for i in range(len(dataBase)):
        employee_email = dataBase["email"][i]
        if (employee_email == userEmail):
            employee_name = dataBase["first_name"][i]
            employee_id = dataBase["idemp"][i]
            curr_employee = employee_class.Employee(employee_name, employee_email, employee_id)
            return curr_employee
    return False

# Search for employee using his ID
# Receive String userID
# Return Employee userID was found
# Return False if it wasn't
def getEmployeePerID(userID):
    dataBase = pd.read_csv('employee_db.csv')
    for i in range(len(dataBase)):
        employee_id = dataBase["idemp"][i]
        if (employee_id == userID):
            employee_name = dataBase["first_name"][i]
            employee_email = dataBase["email"][i]
            curr_employee = employee_class.Employee(employee_name, employee_email, employee_id)
            return curr_employee
    return False

# Modify userID's name
# Receive Int userID, String newName
# Return True if it has been changed
# Return False, if it hasn't
def setEmployeeName(userID, newName):
    dataBase = pd.read_csv('employee_db.csv')
    for i in range(len(dataBase)):
        employee_id = dataBase["idemp"][i]
        if (employee_id == userID):
            # Change Employee Name
            dataBase["first_name"][i] = newName
            # Save new value
            dataBase.to_csv('./employee_db.csv', index=False)
            return True
    # UserID not found
    return False

# Modify userID's email
# Receive Int userID, String newEmail
# Return True if it has been changed
# Return False, if it hasn't
def setEmployeeEmail(userID, newEmail):
    dataBase = pd.read_csv('employee_db.csv')
    for i in range(len(dataBase)):
        employee_id = dataBase["idemp"][i]
        if (employee_id == userID):
            # Change Employee Email
            dataBase["email"][i] = newEmail
            # Save new value
            dataBase.to_csv('./employee_db.csv', index=False)
            return True
    # UserID not found
    return False

# Delete employee corresponding for userID in database
# Receive int userID
# Return True if he was deleted
# Return False if he wasn't
def deleteEmployee(userID):
    userIDfound = False
    dataBase = pd.read_csv('employee_db.csv')
    newDB = pd.DataFrame(columns=['idemp', 'first_name', 'email'])
    for i in range(len(dataBase)):
        currEmployeeName = dataBase["first_name"][i]
        curEmployeeEmail = dataBase["email"][i]
        currEmployeeID = dataBase["idemp"][i]
        if (currEmployeeID != userID):
            newData = [{'idemp': currEmployeeID, 'first_name': currEmployeeName, 'email': curEmployeeEmail}]
            newDB = newDB.append(newData, ignore_index=True)
        if (currEmployeeID == userID):
            userIDfound = True
    newDB.to_csv('./employee_db.csv', index=False)
    return userIDfound

# Add employee corresponding for userID in database
# Receive String userName, String userEmail
# Return True if he was added
# Return False if he wasn't
def addEmployee(userName, userEmail):
    dataBase = pd.read_csv('employee_db.csv')
    userEmailAvailable = emailAvailable(userEmail)
    if (userEmailAvailable):
        employeeId = getNewEmployeeID()
        newData = [{'idemp': employeeId, 'first_name': userName,
                    'email': userEmail}]
        dataBase = dataBase.append(newData, ignore_index=True)
        dataBase.to_csv('./employee_db.csv', index=False)
        return True
    else:
        return False

# Get the next employeeID available in database
# Return int lastUsedID
def getNewEmployeeID():
    dataBase = pd.read_csv('employee_db.csv')
    employeeNum = len(dataBase)
    lastUsedID = dataBase["idemp"][employeeNum - 1]
    return lastUsedID + 1

# Check if email is available or not
# Receive String email
# Return True if it is available
# Return False it is not
def emailAvailable(email):
    dataBase = pd.read_csv('employee_db.csv')
    for i in range(len(dataBase)):
        currEmail = dataBase["email"][i]
        if (currEmail == email):
            return False
    return True

def main():
    employeesList = getAllEmployees()
    for employee in employeesList:
        print(employee)
    print(getEmployeePerEmail("luna@gmail.com"))
    print(getEmployeePerEmail("lunwwa@gmail.com"))
    addEmployee("joao","joao@gmail.com")
    print(pd.read_csv('employee_db.csv'))
    deleteEmployee(2)
    print(pd.read_csv('employee_db.csv'))
main()