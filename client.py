# pip install pyttsx3
import pyttsx3
import importlib
recognizer = importlib.import_module("Codigo_Guigs.3_Recognizer")

def main():
    engine = pyttsx3.init()
    # Call recognizer and get employee name
    #employeeName = recognizer.Recognize()
    employeeName = "Luna"
    engine.say('Good morning, {}'.format(employeeName))
    engine.runAndWait()
main()