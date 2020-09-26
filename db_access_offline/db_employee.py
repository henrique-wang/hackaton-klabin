""""
This file has all functions responsible for checking and editing informations from databases in offline mode
"""

import pandas as pd
import importlib
employee_class = importlib.import_module("classes.employee_class", ".")

# Get all employees from database
# Return List<Employee>
def getAllEmployees():
    dataBase = pd.read_csv('./db_access_offline/employee_db.csv')
    print(dataBase)
    employee_list = []
    for i in range(len(dataBase)):
        employee_name = dataBase["name"][i]
        employee_id = dataBase["iduser"][i]
        employee_email = dataBase["email"][i]
        employee_password = dataBase["password"][i]
        employee_isAdmin = dataBase["admin"][i]
        employee_score = dataBase["score"][i]
        employee_path = dataBase["path"][i]
        employee_picture = dataBase["howmany"][i]
        curr_employee = employee_class.Employee(employee_name, employee_email, employee_password, employee_score,
                                                employee_isAdmin, employee_id, employee_path, employee_picture)
        employee_list.append(curr_employee)
    return employee_list

# Search for employee using his email
# Receive String userEmail
# Return Employee
def getEmployeePerEmail(userEmail):
    dataBase = pd.read_csv('./db_access_offline/employee_db.csv')
    for i in range(len(dataBase)):
        employee_email = dataBase["email"][i]
        if (employee_email == userEmail):
            employee_name = dataBase["name"][i]
            employee_id = dataBase["iduser"][i]
            employee_password = dataBase["password"][i]
            employee_isAdmin = dataBase["admin"][i]
            employee_score = dataBase["score"][i]
            employee_path = dataBase["path"][i]
            employee_picture = dataBase["howmany"][i]
            curr_employee = employee_class.Employee(employee_name, employee_email, employee_password, employee_score,
                                                    employee_isAdmin, employee_id, employee_path, employee_picture)
            return curr_employee
    return False

# Search for employee using his ID
# Receive String userID
# Return Employee userID was found
# Return False if it wasn't
def getEmployeePerID(userID):
    dataBase = pd.read_csv('./db_access_offline/employee_db.csv')
    for i in range(len(dataBase)):
        employee_id = dataBase["iduser"][i]
        if (employee_id == userID):
            employee_name = dataBase["name"][i]
            employee_email = dataBase["email"][i]
            employee_password = dataBase["password"][i]
            employee_isAdmin = dataBase["admin"][i]
            employee_score = dataBase["score"][i]
            employee_path = dataBase["path"][i]
            employee_picture = dataBase["howmany"][i]
            curr_employee = employee_class.Employee(employee_name, employee_email, employee_password, employee_score,
                                                    employee_isAdmin, employee_id, employee_path, employee_picture)
            return curr_employee
    return False

# Modify userID's name
# Receive Int userID, String newName
# Return True if it has been changed
# Return False, if it hasn't
def setEmployeeName(userID, newName):
    dataBase = pd.read_csv('./db_access_offline/employee_db.csv')
    for i in range(len(dataBase)):
        employee_id = dataBase["iduser"][i]
        if (employee_id == userID):
            # Change Employee Name
            dataBase["name"][i] = newName
            # Save new value
            dataBase.to_csv('./db_access_offline/employee_db.csv', index=False)
            return True
    # UserID not found
    return False

# Modify userID's email
# Receive Int userID, String newEmail
# Return True if it has been changed
# Return False, if it hasn't
def setEmployeeEmail(userID, newEmail):
    dataBase = pd.read_csv('./db_access_offline/employee_db.csv')
    for i in range(len(dataBase)):
        employee_id = dataBase["iduser"][i]
        if (employee_id == userID):
            # Change Employee Email
            dataBase["email"][i] = newEmail
            # Save new value
            dataBase.to_csv('./db_access_offline/employee_db.csv', index=False)
            return True
    # UserID not found
    return False

# Delete employee corresponding for userID in database
# Receive int userID
# Return True if he was deleted
# Return False if he wasn't
def deleteEmployee(userID):
    userIDfound = False
    dataBase = pd.read_csv('./db_access_offline/employee_db.csv')
    newDB = pd.DataFrame(columns=['iduser', 'name', 'email', 'password', 'admin', 'score', 'path', 'howmany'])
    for i in range(len(dataBase)):
        employee_id = dataBase["iduser"][i]
        if (employee_id != userID):
            employee_email = dataBase["email"][i]
            employee_password = dataBase["password"][i]
            employee_isAdmin = dataBase["admin"][i]
            employee_score = dataBase["score"][i]
            employee_name = dataBase["name"][i]
            employee_path = dataBase["path"][i]
            employee_picture = dataBase["howmany"][i]
            newData = [{'iduser': employee_id, 'name': employee_name, 'email': employee_email, "password": employee_password,
                        'admin': employee_isAdmin, 'score': employee_score, 'path': employee_path, 'howmany': employee_picture}]
            newDB = newDB.append(newData, ignore_index=True)
        if (employee_id == userID):
            userIDfound = True
    newDB.to_csv('./db_access_offline/employee_db.csv', index=False)
    return userIDfound

# Add employee corresponding for userID in database
# Receive String userName, String userEmail
# Return True if he was added
# Return False if he wasn't
def addEmployee(userName, userEmail, employee_password, employee_isAdmin, employee_score, employee_path, employee_picture):
    dataBase = pd.read_csv('./db_access_offline/employee_db.csv')
    userEmailAvailable = emailAvailable(userEmail)
    if (userEmailAvailable):
        employee_id = getNewEmployeeID()
        newData = [
            {'iduser': employee_id, 'name': userName, 'email': userEmail, "password": employee_password,
             'admin': employee_isAdmin, 'score': employee_score, 'path': employee_path, 'howmany': employee_picture}]
        dataBase = dataBase.append(newData, ignore_index=True)
        dataBase.to_csv('./db_access_offline/employee_db.csv', index=False)
        return True
    else:
        return False

# Get the next employeeID available in database
# Return int lastUsedID
def getNewEmployeeID():
    dataBase = pd.read_csv('./db_access_offline/employee_db.csv')
    employeeNum = len(dataBase)
    lastUsedID = dataBase["iduser"][employeeNum - 1]
    return lastUsedID + 1

# Check if email is available or not
# Receive String email
# Return True if it is available
# Return False it is not
def emailAvailable(email):
    dataBase = pd.read_csv('./db_access_offline/employee_db.csv')
    for i in range(len(dataBase)):
        currEmail = dataBase["email"][i]
        if (currEmail == email):
            return False
    return True

# Receive mysql.connector.connect()
# Update EmployeeList and Return True, if it is connected
# EmployeeList stays the same and Return False, if it isn't connected
def updateEmployeeList(db):
    query = "SELECT * FROM users"
    if (db.is_connected()):
        dataBase = pd.read_sql(query, db)
        dataBase.to_csv('./db_access_offline/employee_db.csv', index=False)
        return True
    else:
        return False

"""
def main():
    employeesList = getAllEmployees()
    #for employee in employeesList:
    #    print(employee)
    #print(getEmployeePerEmail("luna@gmail.com"))
    #print(getEmployeePerEmail("luna@gmail.com"))
    #addEmployee("joao","joao@gmail.com","asd123",1,20,'path/to')
    #print(pd.read_csv('employee_db.csv'))
    #deleteEmployee(2)
    #print(pd.read_csv('employee_db.csv'))
main()
"""