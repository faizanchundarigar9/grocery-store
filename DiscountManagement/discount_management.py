from ConnectDatabase.connect_database import *
from tabulate import tabulate
from datetime import datetime
from Authentication.reg_login import *
from Queries.dm_qry import *

class DiscountManagement():
    
    def discountid_checker(self):
        try:
            did=int(input("Enter Discount coupan id :"))
            qurey_runner(GET_DISCOUNTS_BY_DID_QRY,(did,))
            result=cursor.fetchone()
            if result:
                return 1,did
            else:
                print("Disocunt coupan id not found")
                return -1,0
        except:
            print("discount coupan id not valid")    
            return 0,0
    
    #update discount coupan
    def update_dc(self,did,updated_by):
        ndcode=input("Enter discount copuan : ")
        ns=0
        for i in ndcode:
            if i==" ":
                ns+=1
        if not ndcode:
            print("Discount coupan can't be empty")
        elif len(ndcode)<2 or len(ndcode)>20:
            print("Discount coupan can only between 2 to 20 characters")
        elif ns==len(ndcode):
            print("discount coupan can't be only spaces")
        else:
            qurey_runner(GET_DISCOUNTS_BY_DCODE_QRY,(ndcode,))
            result=cursor.fetchone()
            if result:
                print("discount coupan already exist,enter new discount coupan")
            else:
                qurey_runner(UPDATE_DCODE_QRY,(ndcode,updated_by,did))
                print("Discount Coupan Updated")

    #update discount coupan description            
    def update_dcdescription(self,did,updated_by):
        description=input("Enter new Description : ")
        ns=0
        for i in description:
            if i==" ":
                ns+=1
        if not description:
            print("Description can't be empty")
        elif len(description)<2 or len(description)>35:
            print("Description can only between 2 to 35 characters")
        elif ns==len(description):
            print("Description can't contain only spaces")
        else:
            qurey_runner(UPDATE_DCODE_DESCRIPTION_QRY,(description,updated_by,did))
            print("Description Updated Successfully")

    #update discount coupan percentage
    def update_dcpercentage(self,did,updated_by):
        try:
            percentage=float(input("Enter new Percentage : "))
            if not percentage:
                print("Percentage can't be empty")
            elif percentage>0 and percentage<100:
                qurey_runner(UPDATE_DCODE_PERCENTAGE_QRY,(percentage,updated_by,did))
                print("Description Updated Successfully")                   
        except ValueError:
                print("Percentage is not valid") 

    #update discount coupan valid from 
    def update_dcvalidfrom(self,did,updated_by):
        while True:
            try:
                vf=input("Enter valid from date : ")
                vf = datetime.strptime(vf, '%d-%m-%Y')
                qurey_runner(GET_DCODE_VALIDTO_QRY,(did,))
                result=cursor.fetchone()
            
                if vf > result[0]:
                    print("valid from date can't greater then valid to date")
                else:
                    qurey_runner(UPDATE_DCODE_VALID_FROM_QRY,(vf,updated_by,did))
                    print("Valid From Date Updated Successfully")
                    break
            except ValueError:
                print("Incorrect data format, should be DD-MM-YYYY")               

    #update valid to date 
    def update_dcvalidto(self,did,updated_by):
        try:
            vt=input("Enter valid to date : ")
            vt = datetime.strptime(vt, '%d-%m-%Y')
            qurey_runner(GET_DCODE_VALIDFROM_QRY,(did,))
            result=cursor.fetchone()
            if vt < result[0]:
                print("valid to date can't be lesser than valid from date")
            else:    
                qurey_runner(UPDATE_DCODE_VALID_TO_QRY,(vt,updated_by,did))
                print("Valid to Date Updated Successfully")
        except ValueError:
                print("Incorrect data format, should be DD-MM-YYYY")   

    #update dicount coupan status 
    def update_dcstatus(self,did,updated_by):
        status=["active","inactive"]
        while True:
            print("1 : Update Status to active")                    
            print("2 : Update Status to inactive")
            print("3 : Back")                    
            print("4 : Exit")
            choice=input("Choose one option from the above : ")
            if choice=="1":            
                qurey_runner(GET_DCODE_STATUS_BY_DID_QRY,(did,))
                result=cursor.fetchone()
                if result[0]=="active":
                    print("Discount Coupan is Already Active")
                    break
                else:            
                    qurey_runner(UPDATE_DCODE_STATUS_QRY,(status[0],updated_by,did))
                    print("Status Updated Successfully")
                    break
            elif choice=="2":
                qurey_runner(GET_DCODE_STATUS_BY_DID_QRY,(did,))
                result=cursor.fetchone()
                if result[0]=="inactive":
                    print("Discount Coupan is Already Active")
                    break
                else:            
                    qurey_runner(UPDATE_DCODE_STATUS_QRY,(status[1],updated_by,did))
                    print("Status Updated Successfully")
                    break
            elif choice=="3":
                break
            elif choice=="4":
                final_exit()
            else:
                print("Invalid input, please enter valid input") 

    #update max usage 
    def update_dcmaxusage(self,did,updated_by):
        try:
            mul=float(input("Enter new maximum usage limit : "))
            if not mul:
                print("Maximum usage limit can't be empty")
            elif mul<0:
                print("Maximum usage limit can't be neagtive")
            elif mul>100:
                print("Maximum usage limit can't be greater then 100")    
            else:    
                qurey_runner(UPDATE_DCODE_MAXUSAGE_QRY,(mul,updated_by,did))
                print("Maximum usage limit updated successfully")                   
        except ValueError:
                print("Maximum usage limit is not valid")                      
    def remove_dc(self,did):
        qurey_runner(DELETE_DCODE_QRY,(did,))
        print("Discount coupan removed successfully")            
   
    def discount_coupan_checker(slef,dc):
        qurey_runner(GET_DISCOUNTS_BY_DCODE_QRY,(dc,))
        result=cursor.fetchone()
        if result:
            qurey_runner(GET_DCODE_STATUS_BY_DCODE_QRY,(dc,))
            sts=cursor.fetchone()
            fsts=sts[0]
            if fsts=='active':
                qurey_runner(GET_VALIDATE_DCODE_QRY,(dc,))
                valid=cursor.fetchone()
                if valid:
                    qurey_runner(GET_DCODE_MAXUSAGE_VALIDATE_QRY,(dc,))
                    fstatus=cursor.fetchone()
                    if fstatus:
                        return dc
                    else:
                        print("discount coupan expired 3")
                    #user can apply the code
                else:
                    print("discount coupan expired 2")    
            else:
                print("discount coupan expried 1")
        else:
            print("discount coupan not found")        

    #add new discount coupan
    def add_dc(self):
        ndcode = 0
        description = 0
        percentage=0 
        vf = 0 
        vt = 0
        mul = 0
        fstatus = 0

        #add new coupan
        while True:
            ndcode=input("Enter discount copuan : ")
            ns=0
            for i in ndcode:
                if i==" ":
                    ns+=1
            if not ndcode:
                print("Discount coupan can't be empty")
            elif len(ndcode)<2 or len(ndcode)>20:
                print("Discount coupan can only between 2 to 20 characters")
            elif ns==len(ndcode):
                print("discount coupan can't be only spaces")
            else:
                qurey_runner(GET_DISCOUNTS_BY_DCODE_QRY,(ndcode,))
                result=cursor.fetchone()
                if result:
                    print("discount coupan already exist,enter new discount coupan")
                else:
                   break

        #add coupan description
        while True:
            description=input("Enter description : ")
            ns=0
            for i in description:
                if i==" ":
                    ns+=1
            if not description:
                print("Description can't be empty")
            elif len(description)<2 or len(description)>35:
                print("Description can only between 2 to 35 characters")
            elif ns==len(description):
                print("Description can't contain only spaces")
            else:
                break

        #add discount percentage
        while True:
            try:
                percentage=float(input("Enter percentage : "))
                if not percentage:
                    print("Percentage can't be empty")
                elif percentage>0 and percentage<100:
                    break
            except ValueError:
                print("Percentage is not valid") 

        #add valid from date
        while True:
            try:
                vf=input("Enter valid from date : ")
                if not vf:
                    print("date can't be empty")
                else:
                    vf = datetime.strptime(vf, '%d-%m-%Y')
                    break
            except ValueError:
                print("Incorrect data format, should be DD-MM-YYYY") 

        #add valid to date
        while True:
            try:
                vt=input("Enter valid to date : ")
                if not vt:
                    print("date can't be empty")
                else:
                    vt = datetime.strptime(vt, '%d-%m-%Y')
                    if vt < vf:
                        print("valid to date can't be lesser than valid from date")
                    else:
                        break
            except ValueError:
                print("Incorrect data format, should be DD-MM-YYYY") 

        #add max usage limit    
        while True:    
            try:
                mul=float(input("Enter maximum usage limit : "))
                if not mul:
                    print("Maximum usage limit can't be empty")
                elif mul<0:
                    print("Maximum usage limit can't be neagtive")
                elif mul>100:    
                    print("Maximum usage limit can't be greater than 100")
                else:
                    break
            except ValueError:
                print("Maximum usage limit is not valid") 

        #add coupan status
        status=["active","inactive"]
        while True:
            print("\nCoupan Status")
            print("1 : active")                    
            print("2 : inactive")
            print("3 : Back")                    
            print("4 : Exit")
            choice=input("Choose one option from the above : ")
            if choice=="1":           
                fstatus=status[0]
                break
            elif choice=="2":
                fstatus=status[1]
                break
            elif choice=="3":
                break
            elif choice=="4":
                final_exit()
            else:
                print("Invalid input, please enter valid input")  

        #finally adding coupan
        qurey_runner(ADD_NEW_DCODE_QRY,(ndcode,description,percentage,vf,vt,fstatus,mul))
        print("Coupan code added successfully")