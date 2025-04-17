import mysql.connector
import functions
import sys

#connect to the database with your local host
db = mysql.connector.connect(
    host = "localhost", 
    user = "root",
    password = "root",
    database = "mydb" #<# set the database here to be default using
)
mycursor = db.cursor()

#This To Make The Table
"""
mycursor.execute("CREATE DATABASE mydb") #create the database

mycursor.execute("USE mydb") #use the database, u dont need that if u definded it in the connect

mycursor.execute('''CREATE TABLE contacts (id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(250) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                email VARCHAR(250) NOT NULL DEFAULT "NONE",
                city VARCHAR(250) NOT NULL DEFAULT "NONE")''')  #create the table with some columns
"""

#The Menu function
def menu(db, mycursor):
    while True:
        print("....WELCOME TO YOUR CONTACTS BOOK....\n")
        options = {
            "add_contact": ["1", "add contact"],
            "view_contacts": ["2", "view contacts"],
            "search_contacts": ["3", "search contacts"],
            "delete_contacts": ["4", "delete contacts"],
            "update_contacts": ["5", "update contacts"],
            "quit": ["6", "exit", "quit"]
        }
        print("1-ADD CONTACT 📝\n2=VIEW CONTACTS 📖\n3-SEARCH CONTACT 🔍\n4-DELETE CONTACT 🎯\n5-UPDATE CONTACT 🔄\n6-QUIT 🎱")
        choice =input("Your Option---->: ").strip().lower()
        if choice == "6" or choice == "quit":
            print("\n----GOOD BYE----\n")
            input("----Press Any Key To Continue...----\n")
            sys.exit() 
        for function_name, value in options.items():
            if choice in value:
                fn = getattr(functions, function_name)
                fn(db, mycursor)
                break
        else:  
            print("\n----INVALIDE CHOICE, TRY AGAIN----\n")
            input("----Press Any Key To Continue...----")

menu(db, mycursor)