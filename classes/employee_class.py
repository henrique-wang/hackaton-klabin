""""
This class is used as a reference to get/create an employee properties
"""
class Employee:
    def __init__(self, name, email, id=-1):
        self.employeeName = name
        self.employeeEmail = email
        if (id == -1):
            self.employeeID = 1 #getNewEmployeeID()
        else:
            self.employeeID = id

    def __str__(self):
        string = "ID: {} Name: {} Email: {}".format(self.getEmployeeID(), self.getEmployeeName(),
                                                    self.employeeEmail)
        return string

    def getEmployeeName(self):
        return self.employeeName

    def getEmployeeEmail(self):
        return self.employeeEmail

    def getEmployeeID(self):
        return self.employeeID