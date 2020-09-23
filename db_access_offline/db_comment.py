import pandas as pd
import importlib
from datetime import date
from datetime import datetime
comment_class = importlib.import_module("classes.comment_class", ".")
employee_class = importlib.import_module("classes.employee_class", ".")

# Add comment in database
# Receive String comment, int employeeID
def addComment(employeeID, comment, area, smile):
    dataBase = pd.read_csv('./db_access_offline/employee_comments_db.csv')
    commentID = getNewCommentID()
    today = date.today()
    messageDate = today.strftime("%d/%m/%y")     # dd/mm/YY
    newData = [{'idcom': commentID, 'idemp': employeeID, 'date': messageDate, 'comment': comment,
                    'score': 0, 'area': area, 'smile': smile}]
    dataBase = dataBase.append(newData, ignore_index=True)
    dataBase.to_csv('./db_access_offline/employee_comments_db.csv', index=False)

# Get the next employeeID available in database
# Return int lastUsedID
def getNewCommentID():
    dataBase = pd.read_csv('./db_access_offline/employee_comments_db.csv')
    commentNum = len(dataBase)
    lastUsedID = dataBase["idcom"][commentNum - 1]
    print(lastUsedID)
    return lastUsedID + 1

# Return list of all comments in database
def getAllComments():
    dataBase = pd.read_csv('./db_access_offline/employee_comments_db.csv')
    comment_list = []
    for i in range(len(dataBase)):
        comment_date = datetime.strptime(dataBase["date"][i], '%d/%m/%y')
        curr_employee_id = dataBase["idemp"][i]
        curr_idcom = dataBase["idcom"][i]
        curr_data = dataBase["date"][i]
        curr_comment = dataBase["comment"][i]
        curr_point = dataBase["score"][i]
        curr_area = dataBase["area"][i]
        curr_smile = dataBase["smile"][i]
        comment = comment_class.Comment(curr_employee_id, curr_data, curr_comment, curr_idcom, curr_area, curr_point,
                                        curr_smile)
        comment_list.append(comment)
    return comment_list

# Given a period of time first_date < last_date, this function searchs for comments between these two dates
# Receive String first_date, String last_date (ex: '12/09/2020')
# Return List<Comments>
def getCommentsPerDate(first_date, last_date):
    dataBase = pd.read_csv('./db_access_offline/employee_comments_db.csv')
    minDate = datetime.strptime(first_date, '%d/%m/%y')
    maxDate = datetime.strptime(last_date, '%d/%m/%y')
    comment_list = []
    for i in range(len(dataBase)):
        comment_date = datetime.strptime(dataBase["date"][i], '%d/%m/%y')
        if (comment_date > minDate and comment_date < maxDate):
            curr_employee_id = dataBase["idemp"][i]
            curr_idcom = dataBase["idcom"][i]
            curr_data = dataBase["date"][i]
            curr_comment = dataBase["comment"][i]
            curr_point = dataBase["score"][i]
            curr_area = dataBase["area"][i]
            curr_smile = dataBase["smile"][i]
            comment = comment_class.Comment(curr_employee_id, curr_data, curr_comment, curr_idcom, curr_area, curr_point,
                                            curr_smile)
            comment_list.append(comment)
    return comment_list

# Search for comments which belongs to employee
# Receive Employee employee
# Return List<Comment>
def getCommentsPerEmployee(employee):
    dataBase = pd.read_csv('./db_access_offline/employee_comments_db.csv')
    employeeID = employee.getEmployeeID()
    print("employeeid", employeeID)
    comment_list = []
    for i in range(len(dataBase)):
        curr_employee_id = dataBase["idemp"][i]
        if (employeeID == curr_employee_id):
            curr_idcom = dataBase["idcom"][i]
            curr_data = dataBase["date"][i]
            curr_comment = dataBase["comment"][i]
            curr_point = dataBase["score"][i]
            curr_area = dataBase["area"][i]
            curr_smile = dataBase["smile"][i]
            comment = comment_class.Comment(curr_employee_id, curr_data, curr_comment, curr_idcom, curr_area, curr_point,
                                            curr_smile)
            comment_list.append(comment)

    return comment_list

# Set a new value for comID's point
# Receive int comID, int Point
# Return True if new value was set
# Return False if it wasn't
def setPointForComment(comID, newPoint):
    dataBase = pd.read_csv('./db_access_offline/employee_comments_db.csv')
    for i in range(len(dataBase)):
        curr_comID = dataBase["idcom"][i]
        if (curr_comID == comID):
            # Change Employee Email
            dataBase["score"][i] = newPoint
            # Save new value
            dataBase.to_csv('./db_access_offline/employee_comments_db.csv', index=False)
            return True
    # UserID not found
    return False
"""
def main():
    dataBase = pd.read_csv('employee_comments_db.csv')
    comments = getAllComments()
    for comment in comments:
        print(comment)
    #addComment(1, "funcionou!", "bamoo")
    #print(dataBase)
    #first_date = '19/09/19'
    #last_date = '21/09/19'
    #listcomments = getCommentsPerDate(first_date, last_date)
    #print(listcomments[0])
    #employe = employee_class.Employee('luna','luna@gmail.com','asdaas', 1, 0, 1,'path/to')
    #listcomments = getCommentsPerEmployee(employe)
    #print(listcomments[0])
    #setPointForComment(2, 3)
main()
"""
