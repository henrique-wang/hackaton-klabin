# pip install pyttsx3
import pyttsx3
import importlib
recognizer = importlib.import_module("Codigo_Guigs.3_Recognizer")
employee_db = importlib.import_module("db_access_offline.db_employee", ".")
comment_db = importlib.import_module("db_access_offline.db_comment", ".")
comment_class = importlib.import_module("classes.comment_class", ".")

def main():
    engine = pyttsx3.init()
    # Call recognizer and get employee name
    idusers, idsmile = recognizer.Recognize()
    userName = employee_db.getEmployeePerID(idusers[0])
    engine.say('Boa noite, {}! Qual é a sua sugestão?'.format(userName))
    message = "Message Luna"
    area = "Area Luna"
    smile = 0
    if len(idsmile) > 0:
        if idsmile[0] == idusers[0]:
            smile = 1

    comment_db.addComment(idusers[0], message, area, smile)
    engine.runAndWait()
main()