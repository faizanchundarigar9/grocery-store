from ConnectDatabase.connect_database import *
from tabulate import tabulate
from Authentication.reg_login import final_exit
from Queries.om_qry import*

class OrderManagement():

    #order id checker
    def check_orderid(self):
        try:
            oid=int(input("Enter order id : "))
            qurey_runner(GET_ORDERS_BY_OID_QRY,(oid,))
            result=cursor.fetchone()
            if result:
                return 1,oid
            else:
                print("order id not found")
                return -1,0
        except:
            print("Order id is not valid")
            return -1,0
    #remove orders
    def remove_order(self,oid):
        qurey_runner(REMOVE_ORDER_BY_OID_QRY,(oid,))
        print("Order removes successfully")

    #update order status
    def update_orderstatus(self,oid,updated_by):
        order_statuses=['pedning','shipped','delivered','cancelled']
        while True:
            print("1 : pending")       
            print("2 : shipped")       
            print("3 : delivered")       
            print("4 : cancelled")
            print("5 : Back ")       
            print("6 : Exit ")
            try:
                choice=int(input("Choose one option from the above : "))
                if choice in (1,2,3,4):
                    qurey_runner(UPDATE_ORDER_STATUS_QRY,(updated_by,order_statuses[choice-1],oid))
                    print("Order status updated successfully")    
                elif choice==5:
                    break
                elif choice==6:
                    final_exit()
                else:
                    print("Invalid input, please enter valid input")
            except ValueError:
                print("Invalid input, please enter valid input")        

    #update order total
    def update_ordertotal(self,oid,updated_by):
        try:
            total=int(input("Enter new total : "))
            if total > 1000000:
                print("total is too long")
            else:
                qurey_runner(UPDATE_ORDER_TOTAL_QRY,(total,updated_by,oid)) 
                print("Total updated successfully")   
        except:
            print("Total is not valid")  

    