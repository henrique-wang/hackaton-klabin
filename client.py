# pip install pyttsx3
import pyttsx3
import importlib
recognizer = importlib.import_module("Codigo_Guigs.3_Recognizer")
employee_db = importlib.import_module("db_access_offline.db_employee", ".")
comment_db = importlib.import_module("db_access_offline.db_comment", ".")
comment_class = importlib.import_module("classes.comment_class", ".")
import mysql.connector as mysql
from mysql.connector import Error

try:
    db = mysql.connect(host='localhost',
                       user='root',
                       password='pythaon',
                       database='hackaluna')

    cursor = db.cursor()
    employee_db.updateEmployeeList(db)

except:
  print("An exception occurred")

def main():
    engine = pyttsx3.init()
    # Call recognizer and get employee name
    lista_employee = employee_db.getAllEmployees()
    lista_id = []
    lista_name = []
    for employee in lista_employee:
        lista_id.append(employee.getEmployeeID())
        lista_name.append(employee.getEmployeeName())
    idusers, idsmile = recognizer.Recognize(lista_id,lista_name)
    userName = employee_db.getEmployeePerID(idusers[0]).getEmployeeName()
    engine.say('Que legal, {}! Qual é o nome da sua sugestão?'.format(userName))
    message = "Message Luna"
    area = "Area Luna"
    smile = 0
    if len(idsmile) > 0:
        if idsmile[0] == idusers[0]:
            smile = 1

    comment_db.addComment(idusers[0], message, area, smile)
    comment_db.uploadComment()
    engine.runAndWait()
main()