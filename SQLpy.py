# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 14:04:09 2020

@author: Thomas
"""
import mysql.connector as mysql
from mysql.connector import Error

db = mysql.connect(host='localhost',
                    user='root',
                    password='pythaon',
                   database='hackaluna')

cursor = db.cursor()

def show_all():
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    for table in tables:
        print(table)

def show(database):
    
    order = str(input("Order by?(y/n) "))
    
    if order == 'y':
        category = str(input("Which category? "))
        query = query = "SELECT * FROM " + database + " ORDER BY " + category
    elif order == 'n':
        query = "SELECT * FROM " + database
    
    cursor.execute(query)
    
    table = cursor.fetchall()
    for data in table:
        print(data)

def insert(database):
    query = "SHOW FULL COLUMNS FROM " + database
    cursor.execute(query)
    table = cursor.fetchall()
    print("Here are the columns for this db\n")
    table_inputs = []
    values = "("
    for column in range(len(table)):
        print("\n",table[column][0])
        table_inputs.append(str(input("Input: ")))
        values = values + table_inputs[column]
        if column < len(table)-1:
            values = values + ','
    values = values + ")"
    query = "INSERT INTO " + database + " VALUES " + values + ";"
    
    cursor.execute(query)
    
    db.commit()
    
    print(cursor.rowcount, "data inserted")
    
def delete(database):
    where = str(input("Where: "))
    query = "DELETE FROM " + database + " WHERE " + where
    
    cursor.execute(query)