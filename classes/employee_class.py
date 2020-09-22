""""
This class is used as a reference to get/create an employee properties
"""

class Employee:
    def __init__(self, name, email, password, Score, isAdmin, Id):
        self.employeeName = name
        self.employeeEmail = email
        self.password = password
        self.score = Score
        self.isadmin = isAdmin
        self.id = Id

    def __str__(self):
        string = "ID: {} Name: {} Email: {} isAdmin: {} Points: {} ".format(self.getEmployeeID(), self.getEmployeeName(),
                                                    self.employeeEmail, self.getIsAdmin(), self.getScore())
        return string

    def getEmployeeName(self):
        return self.employeeName

    def getEmployeeEmail(self):
        return self.employeeEmail

    def getEmployeeID(self):
        return self.id

    def getPassword(self):
        return self.password

    def getScore(self):
        return self.score

    def getIsAdmin(self):
        return self.isadmin

    def setAdmin(self, newAdmin):
        self.isadmin = newAdmin

    def setScore(self, newScore):
        self.score = newScore