from Options.options import * 
from ConnectDatabase.connect_database import *
import re
from Queries.quaries import *

class RegLogin():

    @staticmethod
    def login(role):
        # username with vallidation
        username=0
        password=0

        while True:
            username=input("\nEnter your username : ")
            ns=0
            for i in username:
                if i==" ":
                    ns+=1        
            if not username: 
                print("Username can not be empty.")
            elif ns==len(username):
                print("username can't be only spaces")   
            elif len(username) < 2 or len(username) > 25:
                print("Username must be between 2 and 25 characters.")
            elif not re.match("^[A-Za-z0-9 ]+$", username):
                print("Username can only contain letters, numbers and space")
            else:
                #valid username
                break

        while True:
            password=input("\nEnter your password : ")
            if not password:
                print("Password can not be empty.")
            elif len(password) < 3 or len(password) >17:
                print("Password must be between 3 and 17 characters")
            elif not re.match("^[A-Za-z0-9@#._]+$", password):
                print("Password can only contain letters, numbers and #, @, _, .")    
            else:
                #valid password
                break

        #authentication
        qurey_runner(AUTHENTICATION_QRY,(username,password,role))
        user=cursor.fetchone()
        if user:
            return 1,username,user[0]
        else:
            return 0,0,0,
        
def final_exit():
    while True:
        print("\nAre you sure you want to exit")
        print("1 : Yes ")
        print("2 : No \n")
        choice=input()
        if choice=="1":
            raise SystemExit
        elif choice=="2":
            break
        else:
            print(INVALID_INPUT_OPTION)