import mysql.connector 

#add contacts function
def add_contact(db, mycursor):
    print("\n----ADD CONTANTS 📝----\n")
    while True: 
        print("----INSERT THE INFORMATIONS")
        name = input("enter the name: ").strip().lower()
        phone = input("enter the phone: ")
        email = input("enter the email(optional): ").strip().lower()
        city = input("enter the city(optional): ").strip().lower()
        if name == "" or not phone.isdigit():
            print("INVALID VALUE..., TRY AGAIN.")
            
        elif isinstance(email, str) and "@" in email and "." in email or not email:
            try:
                query = "INSERT INTO contacts (name, phone, email, city) VALUES(%s, %s, %s, %s)"
                values = [name, phone, email or "None", city or "None"]
                mycursor.execute(query, (values))
                db.commit()
                if mycursor.rowcount > 0:
                    print("\n---->✅ Contact Has Been Added----\n")
                    mycursor.execute("SELECT * FROM contacts ORDER BY name")
                    for contact in mycursor.fetchall():
                        print(contact)
                    quit = input("---->Type 'Exit' For Exiting OR Press 'ENTER' To Continue....\n").strip().lower()
                    if quit == "exit":
                        break
                else:
                    print("\n---->❌ Contact Has Not Been Added----\n")
                    input("---->Press Any Key To Continue....\n")
            except mysql.connector.Error as err:
                print(f"Something went wrong: {err}")
                input("\n---->Press Any Key To Continue....\n")
        else:
            print("\n---->❌ Invalid Email Format----\n")
            input("---->Press Any Key To Continue....\n")
                

#def contacts update
def update_contacts(db, mycursor):
    print("\n----UPDATE CONTACT 🔄----\n")
    choices = {"1": "name", "2": "phone", "3": "email", "4": "city"}
    u_choice = input("---"*20+"\nWhat Do you wanna change?\n"+"---"*20+"\n1-Name\n2-Phone\n3-Email\n4-City.\n:-- ").strip().lower()

    if u_choice not in choices and u_choice not in choices.values():
        print("\nINVALIDE CHOICE, TRY AGAIN\n")
        input("Press Any Key To Continue...") 
        return
    new_value = input("Enter The New Value: ").strip().lower()
    old_value = input("Enter The Old Value: ").strip().lower()
    try:
        query = (f"UPDATE contacts SET {u_choice} = %s WHERE {u_choice} = %s")
        mycursor.execute(query, (new_value, old_value,))
        db.commit()
        print("\n✅ Contact Has Been Updated\n")
        mycursor.execute("\nSELECT * FROM contacts ORDER BY name\n")
        for contact in mycursor.fetchall():
            print(contact)
        input("Press Enter To Continue...")
    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
        input("Press Any Key To Continue...")
       
#delete contacts 
def delete_contacts(db, mycursor):
    print("\n----DELETE CONTACT 🎯----\n")
    print("\n1-Delete one\n2-Delete all")
    d_choice = input("----Enter your choice---->: ").strip().lower()
    while True:
        if d_choice == "1" or d_choice == "one" or d_choice == "delete one":
            print("----How Do You Wanna Delete----")
            choices = {"1": "id", "2": "name", "3": "phone", "4": "email", "5": "city"}
            choice = input("By:\n1-ID\n2-Name\n3-Phone\n4-Email\n5-City\n----> ").strip().lower()
            if choice not in choices.keys() and choice not in choices.values():
                print("\n----INVALIDE CHOICE, TRY AGAIN----\n")
                input("---->Press Any Key To Continue...\n") 
            else:
                try:    
                    value = input("----Enter The Value u wanna delete----: ").strip().lower()
                    query = (f"DELETE FROM contacts WHERE {choice} = %s")
                    input(f"WARNING: ALL CONTACTS WITH THIS VALUE WILL BE DELETED.\n---->Press Any Key To Continue...\n")
                    mycursor.execute(query, (value,))
                    db.commit()
                    if mycursor.rowcount > 0:
                        print(f"\n----✅ {mycursor.rowcount} Contact Has Been Deleted----\n")
                    else:
                        print(f"{choice} not found, nothing to delete.")
                    mycursor.execute("SELECT * FROM contacts ORDER BY name")
                    result = mycursor.fetchall()
                    for contact in result:
                        print(contact)
                    input("\n---->Press Any Key To Continue...\n")
                    break
                except mysql.connector.Error as err:
                    print(f"Something went wrong: {err}")
                    input("---->Press Any Key To Continue...\n")
                
        elif d_choice == "2" or d_choice == "all" or d_choice == "delete all":
            print("-"*100)
            print("\n----Delete All Contacts----\n")
            print("-"*100)
            input("----ARE YOU SURE? ALL YOUR CONTACT WILL DELETE----\n"
                  "----PRESS ENTER TO CONFIRM----\n")
            mycursor.execute("DELETE FROM contacts")
            db.commit()
            print("\n----✅ All Contacts Have Been Deleted----\n")
            mycursor.execute("SELECT * FROM contacts ORDER BY name")
            for contact in mycursor.fetchall():
                print(contact)
            input("----Press Any Key To Continue...----")
            break
        else:
            print("\n----INVALIDE CHOICE, TRY AGAIN----\n")
            input("----Press Any Key To Continue...----")

#searching for a contact 
def search_contacts(db, mycursor):
    print("\n----SEARCH CONTACT 🔍----\n")
    while True:
        print("\n----How Do You Wanna Find It?")
        s_choice = input("\n1-ID, 2-Name, 3-Phone, 4-Email, 5-City, 6-Quit: \n").strip().lower()
        s_choices = {"id" : ["1","id"],
                     "name" : ["2","name"],
                     "phone" : ["3","phone"],
                     "email" : ["4","email"],
                     "city" : ["5","city"],
                     "quit" : ["6","quit"]
                     }
        if s_choice == "quit" or s_choice == "6":
            print("----->Good Bay<-----")
            return
        field = None
        for key, value in s_choices.items():
                    if s_choice in value:
                        field = key
                                
        if not field:
            print("\n----INVALIDE CHOICE, TRY AGAIN----\n")
            input("----Press Any Key To Continue...----\n")
            
        value = input("----Enter The Value----: \n")
        query = f"SELECT * FROM contacts WHERE {field}=%s"

        mycursor.execute(query, (value,))
        result = mycursor.fetchall()
        
        if result:
            print("HERE WE ARE...")
            for contact in result:
                print(contact)
        else:
            print("\n---->❌ Contact Not Found----\n")
            input("---->Press Any Key To Continue....\n")
            continue
                      
#view all contacts
def view_contacts(db, mycursor):
    print("\n----📖View Contacts----\n")
    try:
        mycursor.execute('SELECT * FROM contacts')
        my_result = mycursor.fetchall()
        for r in my_result:
            print(r)
        input("----Press Any Key To Continue...----")
        return
    except mysql.connector.Error as err:
        print(f"something wrong: {err}")
        
        
        
        

    
        