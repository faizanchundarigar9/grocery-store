from ConnectDatabase.connect_database import *
from Authentication.reg_login import *
from tabulate import tabulate
from Tables.tables import *
import re
from datetime import datetime


class UserManagement():
    #view all users
    @staticmethod
    def view_users():
        qurey="""SELECT user_id as id, username, gender,email, role, TO_CHAR(bdate, 'DD-MM-YYYY') AS birthdate, TO_CHAR(created_at, 'DD Mon YYYY, HH:MI AM') AS "created at",TO_CHAR(updated_at, 'DD Mon YYYY, HH:MI AM') AS "updated at", updated_by as "updated by"FROM Users order by user_id;"""
        cursor.execute(qurey)
        result=cursor.fetchall()
        if result:
            headers = [desc[0] for desc in cursor.description]  # Get column names
            table = tabulate(result, headers, tablefmt='pretty')
            print(table)
        else:
            print("no data found")

    #userid checker
    @staticmethod
    def userid_checker():
        try:
            user_id=int(input("\nEnter userid of user : "))
            qurey="select * from users where user_id=%s"
            qurey_runner(qurey,(user_id,))
            result=cursor.fetchone()
            if result:
                return 1,user_id
            else:
                print("user id not found\n")
                return (0,0)
        except ValueError:
            print("user id not valid\n")
            return (0,0)
        
    #update username
    @staticmethod
    def update_username(user_id,updated_by):
        #new username validation
        print("\nImportant note\n1 : username can't be empty\n2 : username can only contain letters, numbers and space.\n3 : Username must be between 3 and 20 characters")
        username=input("\nEnter new username : ")
        if not username: 
            print("Username cannot be empty.\n")
        elif len(username) < 3 or len(username) > 20:
            print("Username must be between 3 and 20 characters long.\n")
        elif not re.match("^[A-Za-z0-9 ]+$", username):
            print("Username can only contain letters, numbers, and space\n")
        else:
            #valid username
            #checking that entered username alreay exist in the database or not
            qurey_runner(GET_USERNAME_QRY,(username,))
            result = cursor.fetchone()
            if result: # added username already exist
                print("another user exist with the username you entered please add another username")
            else:     
                qurey="UPDATE USERS SET USERNAME=%s,updated_by=%s,updated_at=current_timestamp where user_id=%s"
                qurey_runner(qurey,(username,updated_by,user_id))
                print("username updated successfully\n")

    #email update
    @staticmethod
    def update_email(user_id,updated_by):
        #new email validation
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        email=input("Enter new email : ")
        if not email:
            print("email can't be empty\n")
        elif re.match(pattern, email):
            qurey="UPDATE USERS SET email=%s,updated_by=%s,updated_at=current_timestamp where user_id=%s"
            qurey_runner(qurey,(email,updated_by,user_id))
            print("email updated successfully\n")
        else:
            print("email is not valid\n")

    #gender update        
    @staticmethod
    def update_gender(user_id,updated_by):
        mqurey="UPDATE USERS SET GENDER=%s,updated_by=%s,updated_at=current_timestamp where user_id=%s"
        while True:
            print("1 : Change gender to Male")        
            print("2 : Change gender to Female")        
            print("3 : Back")        
            print("4 : Exit")
            choice=input("Choose one option from above : ")        
            if choice=="1":
                #male update
                qurey="select gender from users where user_id=%s"
                qurey_runner(qurey,(user_id,))
                result=cursor.fetchone()
                if 'male' in result:
                    print("user already male")
                else:    
                    qurey_runner(mqurey,('male',updated_by,user_id))
                    print("Gender updated successfully")
                    break
            elif choice=="2":
                #female update
                qurey="select gender from users where user_id=%s"
                qurey_runner(qurey,(user_id,))
                result=cursor.fetchone()
                if 'female' in result:
                    print("user already female")
                else:    
                    qurey_runner(mqurey,('female',updated_by,user_id))
                    print("Gender updated successfully")
                    break
            elif choice=="3":
                #break
                break
            elif choice=="4":
                final_exit()
            else:
                print("Invalid Input,Please Enter Valid Input")

    #birth date update
    @staticmethod
    def update_bdate(user_id,updated_by):
        bdate=input("Enter new birthdate : ")            
        try:
          if not bdate:
            print("bdate can't be empty")
          else:
            date_obj = datetime.strptime(bdate, '%d-%m-%Y')
            # Get the current date and time
            current_datetime = datetime.now()
            if date_obj > current_datetime :
                print("brithdate can not be in future\n")
            else:    
                qurey="UPDATE USERS SET bdate=TO_DATE(%s,'DD-MM-YYYY'),updated_by=%s,updated_at=current_timestamp where user_id=%s"
                qurey_runner(qurey,(bdate,updated_by,user_id))  
                print("birth date updated successfully")
        except ValueError:
            print("birth date is not valid")  

    #update role
    @staticmethod
    def update_role(user_id,updated_by):
        qurey1="UPDATE USERS SET ROLE=%s,updated_by=%s,updated_at=current_timestamp where user_id=%s"
        qurey2="select role from users where user_id=%s"
        qurey_runner(qurey2,(user_id,))
        result=cursor.fetchone()
        while True:
            print("\n1 : Change Role to Admin")        
            print("2 : Change Role to User")        
            print("3 : Back")        
            print("4 : Exit\n")
            choice=input("Choose one option from above : ")        
            if choice=="1":
                #update role to admin
                if 'admin' in result:
                    print("role is already admin")
                    break
                else:    
                    qurey_runner(qurey1,('admin',updated_by,user_id))
                    print("role updated successfully")
                    break
            elif choice=="2":
                #update role to user
                if 'user' in result:
                    print("role is already user")
                    break
                else:    
                    qurey_runner(qurey1,('user',updated_by,user_id))
                    print("role updated successfully")
                    break
            elif choice=="3":
                #break
                break
            elif choice=="4":
                final_exit()
            else:
                print("Invalid Input,Please Enter Valid Input")
    
    #remove user
    @staticmethod 
    def remove_user(user_id,username):
        qurey="select user_id from users where username=%s"
        qurey_runner(qurey,(username,))
        result=cursor.fetchone()
        if user_id in result:
            while True:
                print("are you sure you want to delte your account")
                print("1 : yes") 
                print("2 : no")
                choice=input("Choose one option from above : ")
                if choice=="1":
                    qurey="DELETE FROM USERS WHERE user_id=%s"
                    qurey_runner(qurey,(user_id,))
                    final_exit()
                elif choice=="2":
                    break
                else:
                    print("Invalid input, please enter valid input")
        else:
            qurey="DELETE CASCADE FROM USERS WHERE user_id=%s"
            qurey_runner(qurey,(user_id,))
            print("user removed successsfully")

    #add new user
    @staticmethod
    def add_user(status):
            
        username=0
        gender=0
        password=0
        role=0
        email=0
        bdate=0
        upi_id=0
        upi_pin=0
        debit_card_number=0
        debit_card_pin=0
        qurey='INSERT INTO USERS (username,password,role,email,gender,bdate) values (%s,%s,%s,%s,%s,%s)'
        #user name validation
        while True:
            print("\nNote\n1 :username can't be empty\n2 : username can only contain letters, numbers, and underscores.\n3 : Username must be between 3 and 20 characters long.\n")
            username=input("Enter new username : ")
            if not username: 
                print("Username cannot be empty.\n")
            elif len(username) < 3 or len(username) > 20:
                print("Username must be between 3 and 20 characters long.\n")
            elif not re.match("^[A-Za-z0-9 ]+$", username):
                print("Username can only contain letters, numbers, and space\n")
            else:
                qurey="select * from users where username=%s"
                qurey_runner(qurey,(username,))
                result=cursor.fetchone()
                if result:
                    print("username already exists,please enter another username")
                else:
                    break

        #password validation
        while True:
            print("\nNote\n1 : Password cannot be empty\n2 : Password must be between 3 and 9 characters long.\n")
            password=input("Enter new password : ")
            if not password:
                print("Password cannot be empty.")
            elif len(password) < 3 or len(password) >13:
                print("Password must be between 3 and 9 characters long.")
            else:
                break

        #email validation
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        while True:
            email=input("\nEnter new email : ")
            if not email:
                print("email can't be empty\n")
            elif re.match(pattern, email):
                break
            else:
                print("email is not valid\n")

        #bdate validation
        while True:
            bdate=input("Enter new birthdate : ")            
            try:  
                if not bdate:
                    print("bdate can't be empty")
                else:
                    date_obj = datetime.strptime(bdate, '%d-%m-%Y')
                    # Get the current date and time
                    current_datetime = datetime.now()
                    if date_obj > current_datetime :
                        print("brithdate can not be in future\n")
                    else:    
                        break
            except:
                print("birth date is not valid")         

        #gender validation
        while True:
            print("\n1 : male")        
            print("2 : female")        
            print("3 : other\n")
            choice=input("choose gender : ")
            if choice=="1":
                gender="male"
                break
            elif choice=="2":
                gender='female'
                break
            elif choice=="3":
                gender="other"
                break
            else:
                print("Invalid input,please enter valid input") 

        # role = "user"        
        if status==1:
            #add new 
            role = "user" 
            qurey_runner(qurey,(username,password,role,email,gender,bdate))        
        elif status==2:
            rqurey="""insert into userregistrationrequests (username,password,email,bdate,role,gender) values (%s,%s,%s,%s,%s,%s);"""
            qurey_runner(rqurey,(username,password,email,date_obj,role,gender))    
            print("Thank You!\n\nYour request has been successfully submitted to the admin for approval. Once approved, you will be notified, and you can log in to your account.")

    #see registration requests
    def update_regrequests(self):
        while True:
            print("1 : View all Registration requests")        
            print("2 : Update registration requests status")        
            print("3 : Back")        
            print("4 : Exit")
            choice=input("Choose one option from the above : ")
            if choice=="1":
                display_table("select * from userregistrationrequests;")
            elif choice=="2":
                    display_table("select * from userregistrationrequests")
                    try:
                        rid=int(input("Enter request id "))
                        qurey="select * from userregistrationrequests where request_id=%s"
                        qurey_runner(qurey,(rid,))
                        result=cursor.fetchone()
                        if result:
                            while True:
                                print("1 : Approve registration request")
                                print("2 : Reject registration request")
                                print("3 : Back")
                                print("4 : Exit")
                                choice=input("Choose one option from the above : ")
                                if choice=="1":
                                    #approve
                                    qurey="UPDATE UserRegistrationRequests SET status = 'approved' WHERE request_id = %s;"
                                    qurey_runner(qurey,(rid,))
                                    qurey="INSERT INTO Users (username, password, email, role, bdate, gender) SELECT username, password, email, role,bdate, gender FROM UserRegistrationRequests WHERE request_id = %s;"
                                    qurey_runner(qurey,(rid,))
                                    print("Registration request approved")
                                    break
                                elif choice=="2":
                                    qurey="UPDATE UserRegistrationRequests SET status = 'rejected' WHERE request_id = %s;"
                                    qurey_runner(qurey,(rid,))
                                    qurey="select username from userregistrationrequests where request_id=%s"
                                    qurey_runner(qurey,(rid,))
                                    result=cursor.fetchone()
                                    qurey="delete from users where username=%s"
                                    qurey_runner(qurey,(result[0],))
                                    print("Registration request rejected")
                                    break
                                elif choice=="3":
                                    break
                                elif choice=="4":
                                    final_exit()
                        else:
                            print("request id not found")
                    except ValueError:
                        print("request id not valid")   
            elif choice=="3":
                break
            elif choice=="4":
                final_exit()
            else:
                print("Invalid input")