from Authentication.reg_login import *
from UserManagement.user_management import *
from ProductManagement.product_management import *
from OrderManagement.order_management import *
from CustomerSupportManagement.customer_support_management import *

class admin(RegLogin,UserManagement,ProductManagement,DiscountManagement,OrderManagement,CustomersupportManagement):
    pass

def run_admin():
    admin_obj = admin()
    result=admin_obj.login('admin')
    if result[0]==1:#succefull login of admin
        print(f"\nLogin successful! You are now in the admin panel, {result[1]}.\nYou can manage the entire grocery store system from this admin panel.")
        while True:#admin features
            print(ADMIN_FEATURES)
            try:
                choice=int(input(CHOICE_OPTION))
                if choice in (1,2,3,4,5,6,7,8):
                    if choice==1:#user management panel
                        while True: #inside user management paneL
                            print(USER_MANAGEMENT_FEATURES)
                            try:
                                choice=int(input(CHOICE_OPTION))
                                if choice in (1,2,3,4,5,6,7):
                                    if choice==1:#view all users
                                        print("\n--- Users List ---")
                                        print("Here is the list of all registered users:\n")
                                        admin_obj.view_users()
                                        print("\n")
                                    elif choice==2:#update user infromation
                                        print("\n--- Users List ---")
                                        print("Here is the list of all registered users:\n")
                                        admin_obj.view_users()
                                        uid_data=admin_obj.userid_checker()
                                        while True:
                                            if uid_data[0]==1:
                                                print(UPDATE_USER_INFO_FEATURES)
                                                try:
                                                    choice=int(input(CHOICE_OPTION))
                                                    if choice in (1,2,3,4,5,6,7):
                                                        if choice==1:#username updation pannel
                                                            admin_obj.update_username(uid_data[1],result[1])   
                                                        elif choice==2:#role updation pannel
                                                            admin_obj.update_role(uid_data[1],result[1])
                                                        elif choice==3:#email updation pannel
                                                            admin_obj.update_email(uid_data[1],result[1])
                                                        elif choice==4:#birthdate updation pannel
                                                            admin_obj.update_bdate(uid_data[1],result[1])
                                                        elif choice==5:#gender updation pannel
                                                            admin_obj.update_gender(uid_data[1],result[1])
                                                        elif choice==6:#back
                                                            break
                                                        elif choice==7:
                                                            final_exit()
                                                        else:
                                                            print(INVALID_INPUT_OPTION)
                                                    else:
                                                        print(INVALID_INPUT_OPTION)        
                                                except ValueError:
                                                    print(INVALID_INPUT_OPTION)     
                                            else:
                                                break
                                    elif choice==3:
                                        #remove 
                                        print("\n--- Users List ---")
                                        print("Here is the list of all registered users:\n")
                                        admin_obj.view_users()
                                        uid_data=admin_obj.userid_checker()
                                        if uid_data[0]==1:
                                            admin_obj.remove_user(uid_data[1],result[1])
                                        else:
                                            pass
                                    elif choice==4:
                                        #add new user
                                        admin_obj.add_user(1)
                                        pass
                                    elif choice==5:
                                        admin_obj.update_regrequests()
                                    elif choice==6:
                                        #back
                                        break
                                    elif choice==7:
                                        #final exit from the system
                                        final_exit()
                                    else:
                                        print("Please enter a valid option (1-6).\n") 
                            except ValueError:
                                print(INVALID_INPUT_OPTION)                       
                    elif choice==2:#category management panel
                        while True:
                            update_category_status()
                            print(CATEGORY_MANAGEMENT_FEATURES)
                            try:
                                choice=int(input(CHOICE_OPTION))
                                if choice in (1,2,3,4,5,6):
                                    if choice==1:
                                        display_table(DISPLAY_CATEGORIES_QRY)
                                    elif choice==2:
                                        display_table(DISPLAY_CATEGORIES_QRY)
                                        cid_check=admin_obj.check_categoryid()
                                        if cid_check[0]==1:
                                            while True:
                                                print("1 : Update Category Name")
                                                print("2 : Update Category Description")   
                                                print("3 : Break") 
                                                print("4 : Exit") 
                                                try:   
                                                    choice=int(input(CHOICE_OPTION))
                                                    if choice==1:#update category name
                                                        admin_obj.update_category_name(cid_check[1],result[1])
                                                    elif choice==2:#update category description
                                                        admin_obj.update_category_description(cid_check[1],result[1])
                                                    elif choice==3:
                                                        break
                                                    elif choice==4:
                                                        final_exit()
                                                    else:
                                                        print(INVALID_INPUT_OPTION)
                                                except ValueError:
                                                    print(INVALID_INPUT_OPTION)        
                                        else:
                                            pass  
                                    elif choice==3:
                                        admin_obj.remove_category()
                                    elif choice==4:
                                        admin_obj.add_category()              
                                    elif choice==5:
                                        break
                                    elif choice==6:
                                        final_exit()
                                    else:
                                        print(INVALID_INPUT_OPTION)
                            except ValueError:
                                print(INVALID_INPUT_OPTION)     
                    elif choice==3:#product management panel
                            while True:
                                update_category_status()
                                print(PRODUCT_MANAGEMENT_FEATURES)
                                try:
                                    choice=int(input(CHOICE_OPTION))
                                    if choice in (1,2,3,4,5,6):
                                        if choice==1:#view all products
                                            while True:
                                                print("\nlist of categories")
                                                display_table(DISPLAY_CATEGORIES_QRY)
                                                cid_result=admin_obj.check_categoryid()
                                                if cid_result[0]==1:
                                                    admin_obj.view_products(f"""SELECT p.product_id as "product id", p.name AS "product name", p.description,'₹' || p.price as price, CONCAT(p.stock,' ',p.base_quantity) as stock, c.name AS "category name",TO_CHAR(p.created_at, 'DD Mon YYYY, HH:MI AM') AS "created at",TO_CHAR(p.updated_at, 'DD Mon YYYY, HH:MI AM') AS "updated at", p.updated_by as "updated by" FROM Products p JOIN Categories c ON p.category_id = c.category_id where c.category_id={cid_result[1]};""")
                                                    break            
                                        elif choice==2: #update products
                                            print("\nlist of categories")
                                            display_table(DISPLAY_CATEGORIES_QRY)
                                            cid_result=admin_obj.check_categoryid()
                                            if cid_result[0]==1:
                                                admin_obj.view_products(f"""SELECT p.product_id as "product id", p.name AS "product name", p.description,'₹' || p.price as price, CONCAT(p.stock,' ',p.base_quantity) as stock, c.name AS "category name",TO_CHAR(p.created_at, 'DD Mon YYYY, HH:MI AM') AS "created at",TO_CHAR(p.updated_at, 'DD Mon YYYY, HH:MI AM') AS "updated at", p.updated_by as "updated by" FROM Products p JOIN Categories c ON p.category_id = c.category_id where c.category_id={cid_result[1]};""")
                                                pid_check=admin_obj.check_productid()
                                                if pid_check[0]==1:
                                                    while True:
                                                        print("1 : Update Product Name ")
                                                        print("2 : Update Product Description")
                                                        print("3 : Update Product Stock")
                                                        print("4 : Update Product Category ID")
                                                        print("5 : Update Product Price")
                                                        print("6 : Back")
                                                        print("7 : Exit")
                                                        choice=int(input(INVALID_INPUT_OPTION))
                                                        if choice==1: #update product name
                                                            admin_obj.update_product_name(pid_check[1],result[1])
                                                        elif choice==2: #update product description
                                                            admin_obj.update_product_description(pid_check[1],result[1])
                                                        elif choice==3: #update product stock
                                                            admin_obj.update_product_stock(pid_check[1],result[1])
                                                        elif choice==4: #update category id
                                                            admin_obj.update_product_categoryid(pid_check[1],result[1])
                                                        elif choice==5: #update product price
                                                            admin_obj.update_product_price(pid_check[1],result[1])
                                                        elif choice==6: #back
                                                            break
                                                        elif choice==7:
                                                            final_exit() 
                                        elif choice==3: #add new product
                                            update_category_status()
                                            admin_obj.add_product()
                                        elif choice==4: #remove product
                                            print("\nlist of categories")
                                            display_table(DISPLAY_CATEGORIES_QRY)
                                            cid_result=admin_obj.check_categoryid()
                                            if cid_result[0]==1:
                                                admin_obj.view_products(f"""SELECT p.product_id as "product id", p.name AS "product name", p.description,'₹' || p.price as price, CONCAT(p.stock,' ',p.base_quantity) as stock, c.name AS "category name",TO_CHAR(p.created_at, 'DD Mon YYYY, HH:MI AM') AS "created at",TO_CHAR(p.updated_at, 'DD Mon YYYY, HH:MI AM') AS "updated at", p.updated_by as "updated by" FROM Products p JOIN Categories c ON p.category_id = c.category_id where c.category_id={cid_result[1]};""")
                                                admin_obj.remove_product()
                                                break
                                        elif choice==5: #back
                                            break
                                        elif choice==6:
                                            final_exit()
                                        else:
                                            print(INVALID_INPUT_OPTION)
                                    else:
                                        print(INVALID_INPUT_OPTION)        
                                except ValueError:
                                    print(INVALID_INPUT_OPTION)            
                    elif choice==4: #discount management panel
                        while True:
                            print(DISCOUNT_MANAGEMENT_FEATURES)
                            try:
                                choice=int(input(CHOICE_OPTION))
                                if choice in (1,2,3,4,5,6):
                                    if choice==1:
                                        display_table(DISPLAY_DSICOUNT_CODES_QRY)
                                    elif choice==2:
                                        #update discount coupan
                                        did_check=admin_obj.discountid_checker()
                                        if did_check[0]==1:
                                            while True:
                                                print(DISCOUNT_COUPAN_UPDATE_FEATURES)
                                                try:
                                                    choice=int(input(CHOICE_OPTION))
                                                    if choice in (1,2,3,4,5,6,7,8,9):
                                                        if choice==1:
                                                            admin_obj.update_dc(did_check[1],result[1])
                                                        elif choice==2:
                                                            admin_obj.update_dcdescription(did_check[1],result[1])    
                                                        elif choice==3:
                                                            pass
                                                        elif choice==4:
                                                            admin_obj.update_dcvalidfrom(did_check[1],result[1])
                                                        elif choice==5:
                                                            admin_obj.update_dcvalidto(did_check[1],result[1]) 
                                                        elif choice==6:
                                                            admin_obj.update_dcstatus(did_check[1],result[1])       
                                                        elif choice==7:
                                                            admin_obj.update_dcmaxusage(did_check[1],result[1])    
                                                        elif choice==8:
                                                            break
                                                        elif choice=="9":
                                                            final_exit()
                                                        else:
                                                            print(INVALID_INPUT_OPTION)
                                                    else:
                                                        print(INVALID_INPUT_OPTION)    
                                                except ValueError:
                                                    print(INVALID_INPUT_OPTION)              
                                        else:
                                            pass   
                                    elif choice==3:
                                        result=admin_obj.discountid_checker()
                                        if result[0]==1:
                                            admin_obj.remove_dc(result[1])
                                        else:
                                            pass 
                                    elif choice==4:
                                        admin_obj.add_dc()       
                                    elif choice==5:
                                        break
                                    elif choice==6:
                                        final_exit()
                                    else:
                                        print(INVALID_INPUT_OPTION)  
                                else:
                                    print(INVALID_INPUT_OPTION)  
                            except ValueError:
                                print(INVALID_INPUT_OPTION)                  
                    elif choice==5: #order management panel
                        while True:
                            print("Order management panel")
                            print(ORDER_MANAGEMENT_FEATURES)
                            try:
                                choice=int(input(CHOICE_OPTION))
                                if choice==1: #view orders
                                    display_table(DISPLAY_ORDERS_QRY)
                                elif choice==2: #update order
                                    rp=admin_obj.check_orderid()
                                    if rp[0]==1:
                                        while True:
                                            print(ORDER_UPDATE_FEATURES)
                                            try:
                                                choice=int(input(CHOICE_OPTION))
                                                if choice==1:
                                                    admin_obj.update_orderstatus(rp[1],result[1])
                                                elif choice==2:
                                                    admin_obj.update_ordertotal(rp[1],result[1])
                                                elif choice==3:
                                                    break
                                                elif choice==4:
                                                    final_exit()
                                                else:
                                                    print(INVALID_INPUT_OPTION)     
                                            except ValueError:
                                                print(INVALID_INPUT_OPTION)                     
                                elif choice==3: #remove order
                                    pass
                                elif choice==4:
                                    break
                                elif choice==5:
                                    final_exit()
                                else:
                                    print(INVALID_INPUT_OPTION)       
                            except ValueError:
                                print(INVALID_INPUT_OPTION)                    
                    elif choice==6: #customer support panel
                        while True:
                            print("Customer Support Panel")
                            try:
                                choice=int(input(CHOICE_OPTION))
                                if choice in (1,2,3,4,5,6,7):
                                    if choice==1:
                                        admin_obj.view_support_ticekts()
                                    elif choice==2:
                                        admin_obj.view_support_responses()   
                                    elif choice==3:
                                        admin_obj.update_supportt_status(result[1])
                                    elif choice==4:
                                        admin_obj.update_supportr_message(result[1])
                                    elif choice==5:
                                        admin_obj.provide_supportt_response()    
                                    elif choice==6:
                                        break    
                                    elif choice==7:
                                        final_exit()
                                    else:
                                        print(INVALID_INPUT_OPTION)
                                else:
                                    print(INVALID_INPUT_OPTION)
                            except ValueError:
                                print(INVALID_INPUT_OPTION)                 
                    elif choice==7: #back
                        break
                    elif choice==8: #final exit from system
                        final_exit() 
                    else:
                        print(INVALID_INPUT_OPTION) 
                else: #else for the incoorect password
                    print("username or password is incorrect")
            except ValueError:
                print(INVALID_INPUT_OPTION)  
    else:
        print("username or password is incorrect")                  
