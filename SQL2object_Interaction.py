# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 18:29:44 2020

@author: Thomas
"""

from datetime import datetime
from datetime import date
import importlib
employee_class = importlib.import_module("classes.employee_class", ".")
comment_class = importlib.import_module("classes.comment_class", ".")

#Conexão com o banco de dados do localhost 
import mysql.connector as mysql
from mysql.connector import Error

db = mysql.connect(host='localhost',
                    user='root',
                    password='pythaon',
                   database='hackaluna')

cursor = db.cursor()

def db_2_comment(item):
    date = item[2]
    messageDate = date.strftime("%d/%m/%y")
    comment = comment_class.Comment(item[1],date,item[3],item[0],item[4],item[6],item[5])
    return comment
    
def db_2_employee(item):  
    employee = employee_class.Employee(item[1],item[2],item[3],item[6],item[5],item[0],item[4])
    return employee

#DATABASE EMPLOYEES (users)
################################################################################
#FROM INTERFACE TO DB
def employee_2_db(employee):
    #colocar informação de outra colunas
    
    values = "("+str(employee.getEmployeeID())+",'"+employee.getEmployeeName()\
        +"','"+employee.getEmployeeEmail()+"','"+employee.getPassword()+"','"\
        +employee.getPhotoPath()+"',"+str(employee.getIsAdmin())+","\
            +str(employee.getScore())+")"
    
    query = "INSERT INTO users VALUES " + values + ";"
    
    cursor.execute(query)
    
    db.commit()
    
def update_employee_db(employee):
    where = "iduser = " + str(employee.getEmployeeID())
    update = "name='"+employee.getEmployeeName()+"',email='"+employee.getEmployeeEmail()\
        +"',password='"+employee.getPassword()+"',path='"+employee.getPhotoPath()\
            +"',admin="+str(employee.getIsAdmin())+",score="+str(employee.getScore())
    query = "UPDATE users SET " + update + " WHERE " + where
    
    cursor.execute(query)
    
    db.commit()
    
def delete_employee_db(employee):
    query = "DELETE FROM users WHERE iduser = " + str(employee.getEmployeeID())
    
    cursor.execute(query)
    
    db.commit()
    
#FROM DB TO INTERFACE

def show_employee_id_order():
    query = "SELECT * FROM users ORDER BY iduser"       
    cursor.execute(query)
    
    table = cursor.fetchall()
    
    lista = []
    
    for item in table:
        lista.append(db_2_employee(item))
    return lista
    
        
def show_employee_name_order(): #dos usuarios
    query = "SELECT * FROM users ORDER BY name"
    
    cursor.execute(query)
    
    table = cursor.fetchall()
    
    list_employee = []
    
    for item in table:
        list_employee.append(db_2_employee(item))
    
    return list_employee
    
def fetch_by_id(iduser):
    query = "SELECT * FROM users WHERE iduser = " + str(iduser)
    
    cursor.execute(query)
    
    table = cursor.fetchall()
    
    employee = db_2_employee(table[0])
    
    return employee

def fetch_by_email(email):
    query = "SELECT * FROM users WHERE iduser = '" + email + "'"
    
    cursor.execute(query)
    
    table = cursor.fetchall()
    
    employee = db_2_employee(table[0])
    
    return employee

#DATABASE COMMENTS (comments)
################################################################################
def comment_2_db(comment):
    #colocar informação de outra colunas
    
    date = datetime.strptime(comment.getDate(), '%d/%m/%y').date()
    
    values = "("+str(comment.getCommentID())+","+str(comment.getUserID())\
        +",'"+str(date)+"','"+comment.getMessage()+"','"\
        +comment.getArea()+"',"+str(comment.getScore())+","\
            +str(comment.getSmile())+")"
    
    query = "INSERT INTO comments VALUES " + values + ";"
    
    cursor.execute(query)
    
    db.commit()
    
def update_comment_db(comment):
    
    date = datetime.strptime(comment.getDate(), '%d/%m/%y').date()
    
    where = "idcom = " + str(comment.getCommentID())
    update = "iduser="+str(comment.getUserID())+",date="+str(date)\
        +",comment='"+comment.getMessage()+"',area='"+comment.getArea()\
            +"'',score="+str(comment.getScore())+",smile="+str(comment.getSmile())
    query = "UPDATE comments SET " + update + " WHERE " + where
    
    cursor.execute(query)
    
    db.commit()
    
def delete_employee_db(comment):
    query = "DELETE FROM comments WHERE idcom = " + str(comment.getCommentID())
    
    cursor.execute(query)
    
    db.commit()   

#FROM DB TO INTERFACE

def show_comment_id_order():
    query = "SELECT * FROM comments ORDER BY idcom"       
    cursor.execute(query)
    
    table = cursor.fetchall()
    
    lista = []
    
    for item in table:
        lista.append(db_2_comment(item))
    return lista

def show_comment_iduser_order(): #dos usuarios
    query = "SELECT * FROM comments ORDER BY iduser"
    
    cursor.execute(query)
    
    table = cursor.fetchall()
    
    print(table)
    
    lista = []
    
    for item in table:
        lista.append(db_2_comment(item))
    
    return lista

def show_comment_date_order():
    query = "SELECT * FORM comments ORDER BY date"
    
    cursor.execute(query)
    
    table = cursor.fetchall()
    
    lista = []
    
    for item in table:
        lista.append(db_2_comment(item))
    return lista
    
def show_comment_area_order():
    query = "SELECT * FROM comments ORDER BY area"
    
    cursor.execute(query)
    
    table = cursor.fetchall()
    
    lista = []
    
    for item in table:
        lista.append(db_2_comment(item))
        
    return lista





