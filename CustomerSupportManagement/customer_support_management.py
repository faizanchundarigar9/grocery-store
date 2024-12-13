from ConnectDatabase.connect_database import *
from Tables.tables import *
import re
from Authentication.reg_login import final_exit
from Queries.csm_qry import *

class CustomersupportManagement():
    
    #update support ticket status
    def update_supportt_status(self,updated_by):    
        try:
            tid=int(input("Enter ticket id : "))
            statuses=['open','closed','in progress']
            qurey_runner(GET_STS_BY_TID_QRY,(tid,))
            result=cursor.fetchone()
            if result:
                while True:
                    print("1 : Update Status to Open")
                    print("2 : Update status to Closed")
                    print("3 : Update Status to In progress")
                    print("4 : Back")
                    print("5 : Exit")
                    choice=input("Choose one option from above : ")
                    if choice=="1":
                        qurey_runner(GET_ST_STATUS_BY_TID_QRY,(tid,))
                        result=cursor.fetchone()
                        if result[0]=="open":
                            print("Ticket status is already open")
                            break
                        else:
                            qurey_runner(UPDATE_ST_STATUS_QRY,(statuses[0],updated_by,tid))    
                            print("Status updated successfully")
                            break
                    elif choice=="2":
                        qurey_runner(GET_ST_STATUS_BY_TID_QRY,(tid,))
                        result=cursor.fetchone()
                        if result[0]=="closed":
                            print("Ticket status is already  closed")
                            break
                        else:
                            qurey_runner(UPDATE_ST_STATUS_QRY,(statuses[1],updated_by,tid))    
                            print("Status updated successfully")
                            break
                    elif choice=="3":
                        qurey_runner(GET_ST_STATUS_BY_TID_QRY,(tid,))
                        result=cursor.fetchone()
                        if result[0]=="in progress":
                            print("Ticket status is already in progress")
                            break
                        else:
                            qurey_runner(UPDATE_ST_STATUS_QRY,(statuses[2],updated_by,tid))    
                            print("Status updated successfully")  
                            break     
                    elif choice=="4":
                        break
                    elif choice=="5":
                        final_exit()
                    else:
                        print("Invalid input,Please enter valid input")   
            else:
                print("ticekt id not found")
        except ValueError:
            print("Ticekt id is not valid") 

    #update support response message
    def update_supportr_message(self,updated_by):
        try:
            rid=int(input("Enter reponse id : "))
            qurey_runner(GET_SR_BY_RID_QRY,(rid,))
            result=cursor.fetchone()
            if result:
                while True:
                    msg=input("Enter new message : ")
                    if not msg:
                        print("response message can't be empty")
                    elif len(msg)<2:
                        print("response message can't be too short")
                    elif len(msg)>50:
                        print("response message can't too long")
                    elif not re.match("^[A-Za-z0-9 ]+$",msg):
                        print("response message can only contain letters, numbers, and space\n")
                    else:
                        qurey_runner(UPDATE_SR_MESSAGE_QRY,(msg,updated_by,rid))
                        print("response message updated successfully")
                        break
            else:
                print("Response id not found")
        except ValueError:
            print("Response id is not valid")    

    #provide support ticket responses
    def provide_supportt_response(self):
        tid=0
        message=0
        try:
            tid=int(input("Enter ticket id : "))
            qurey_runner(GET_STS_BY_TID_QRY,(tid,))
            result=cursor.fetchone()
            if result:
                while True:
                    message=input("Enter the message for support ticket : ")
                    if not message:
                        print("message can't be empty")
                    elif len(message)>35:
                        print("message is too long")
                    elif len(message)<=2:
                        print("message is too short")
                    elif not re.match("^[A-Za-z0-9 ]+$", message):
                        print("message can only contain letters,numbers and space\n")
                    else:
                        qurey_runner(INSERT_SR_QRY,(message,tid))
                        print("Response message added successfully")
                        break                  
            else:
                print("Ticket id is not found")    
        except ValueError:
            print("Ticket id is not valid")    
    #generate support ticket by user
    def generate_supportticket(self,uid):
        subject=0
        message=0
        while True:
            subject=input("Enter the subject for support ticket : ")
            if not subject:
                print("subject can't be empty")
            elif len(subject)>35:
                print("Subject is too long")
            elif len(subject)<=2:
                print("Subject is too short")
            elif not re.match("^[A-Za-z ]+$", subject):
                print("subject can only contain letters and space\n")
            else:
                break
        while True:
            message=input("Enter the message for support ticket : ")
            if not subject:
                print("message can't be empty")
            elif len(message)>45:
                print("message is too long")
            elif len(message)<=2:
                print("message is too short")
            elif not re.match("^[A-Za-z0-9 ]+$", message):
                print("message can only contain letters,numbers and space\n")
            else:
                break  
        qurey_runner(INSERT_ST_QRY,(subject,message,uid)) 
        print("Support ticket generated successfully")