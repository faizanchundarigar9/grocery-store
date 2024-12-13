from ConnectDatabase.connect_database import *
from Options.options import *
from Authentication.reg_login import *
from Admin.admin import *
from User.user import *

#creating object for admin
admin_object = admin() 

if db_cnn: #if the database connected successfully then procced
    print("\nWelcome to Grocery Store\n")
    while True: # login,register,exit page
        print("\n1 : Admin") 
        print("2 : Userr")
        print("3 : Exit")
        try:
            choice=int(input(CHOICE_OPTION))
            if choice in (1,2,3): #proceed 
                if choice==1: #admin panel
                    while True:
                        print(ADMIN_OPTIONS)
                        try:
                            choice=int(input(CHOICE_OPTION))
                            if choice in (1,2,3):
                                if choice==1: #login for admin
                                    run_admin()
                                elif choice==2: #one step back
                                    break
                                elif choice==3: #final exit from the system
                                    final_exit()
                            else:
                                print(INVALID_INPUT_OPTION)
                        except ValueError:
                            print(INVALID_INPUT_OPTION)
                elif choice==2: #user panel
                    while True:
                        print(USER_OPTIONS)
                        try:
                            choice=int(input(CHOICE_OPTION))
                            if choice in (1,2,3,4):
                                if choice==1: #user login
                                    run_user()
                                elif choice==2: # user registration
                                    nuser_obj  = user()
                                    nuser_obj.add_user(2)
                                    pass
                                elif choice==3: # back
                                    break
                                elif choice==4: # exit
                                    final_exit()
                                else:
                                    print(INVALID_INPUT_OPTION)
                            else:
                                print(INVALID_INPUT_OPTION)
                        except ValueError:
                            print(INVALID_INPUT_OPTION)                
                elif choice==3: #fina exit from the system
                    final_exit()
            else:
                print(INVALID_INPUT_OPTION)
        except ValueError:
            print(INVALID_INPUT_OPTION)
else:
    #if the database is not connected 
    print("databse is not connected")
    pass