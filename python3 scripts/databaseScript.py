# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 23:48:19 2020

@author: amine gasa
"""
import sqlite3
from datetime import datetime
conn=sqlite3.connect('databaseAttendance.db')
c = conn.cursor()
           
def create_data():
    with conn:
           c.execute("""CREATE TABLE if not exists Attendance (	"id" INTEGER PRIMARY KEY AUTOINCREMENT,	"fullname"	TEXT NOT NULL,	"datetime"	NUMERIC NOT NULL);""")

def insert_data(name,datetime):
    with conn:
        c.execute(f"INSERT INTO Attendance  (fullname , datetime)values ('{name}','{datetime}');")                   
        
def exist_name(name,d1):
          c.execute(f"SELECT fullname FROM Attendance  where datetime between '{d1} 00:00:00' and '{d1} 23:59:59' ")
          row =c.fetchall()
          for ro in row:
              if(name==ro[0]):
                  return True
          return False

       
