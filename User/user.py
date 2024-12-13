from Authentication.reg_login import *
from ProductManagement.product_management import *
from UserManagement.user_management import *
from CustomerSupportManagement.customer_support_management import *

class user(RegLogin,ProductManagement,UserManagement,CustomersupportManagement,MyPDF):
    pass

def run_user():
    user_obj = user()
    result = user_obj.login('user')
    if result[0]==1:
        user_obj.cart_creation(result[2])
        user_obj.wishlist_creation(result[2])
        print(f"Welcome back, {result[1]}! You have successfully logged in.")
        while True:
            print(USER_FEATURES)
            try:
                choice=int(input(CHOICE_OPTION))
                if choice in (1,2,3,4,5,6,7,8):
                    if choice==1: #view products by category
                        while True:
                            print(VIEW_PRODUCTS_FEATURES)
                            choice=int(input(CHOICE_OPTION))
                            if choice==1: #view and add to cart product by cateogory
                                print("\nlist of categories")
                                display_table(DISPLAY_ACTIVE_CATEGORIES_QRY)
                                cid_result=user_obj.check_categoryid()
                                if cid_result[0]==1:
                                    while True:
                                        user_obj.view_products(f"""SELECT p.product_id as "product id", p.name AS "product name", p.description, p.price || '₹' price, CONCAT(p.stock,' ',p.base_quantity) as stock, c.name AS "category name" FROM Products p JOIN Categories c ON p.category_id = c.category_id where c.category_id={cid_result[1]} and p.stock > 0;""")
                                        print("1 : Add to cart")
                                        print("2 : Add to wishlist")
                                        print("3 : Back")
                                        print("4 : Exit")
                                        try:
                                            choice=int(input(CHOICE_OPTION))
                                            if choice in (1,2,3,4):
                                                if choice==1: #add to cart
                                                    user_obj.add_to_cart(result[2])
                                                elif choice==2: # add to wishlist
                                                    user_obj.add_to_wishlist(result[2])
                                                elif choice==3: #back
                                                    break
                                                elif choice==4:
                                                    final_exit()
                                                else:
                                                    print(INVALID_INPUT_OPTION)
                                            else:
                                                print(INVALID_INPUT_OPTION)
                                        except ValueError:
                                            print(INVALID_INPUT_OPTION)                
                            elif choice==2: #back
                                break
                            elif choice==3:
                                final_exit()
                            else:
                                print(INVALID_INPUT_OPTION)
                    elif choice==2: #Manage cart
                        while True:
                            print("\n1 : View cart")
                            print("2 : Remove item from cart")
                            print("3 : Checkout")
                            print("4 : Back")
                            print("5 : Exit")
                            try:
                                choice=int(input(CHOICE_OPTION))
                                if choice in (1,2,3,4,5):
                                    if choice==1:
                                        display_table(f"""SELECT p.product_id as "product id",p.name as "product name",'₹' || ci.price_at_addition as "price per unit", ci.quantity || ' ' || ci.base_quantity AS quantity,'₹' || ci.price_at_addition*ci.quantity as "net amount",ROUND(ci.tax_rate,0) || '%' as "tax rate",ci.tax_type as "tax type",'₹' || ROUND(((ci.price_at_addition*ci.quantity)*ci.tax_rate)/100,2) as "tax amount",'₹' || ROUND((((ci.price_at_addition*ci.quantity)*ci.tax_rate)/100+ci.price_at_addition*ci.quantity),2) as "total amount"  FROM CartItems ci JOIN Products p ON ci.product_id = p.product_id JOIN Cart c ON ci.cart_id = c.cart_id WHERE c.user_id = {result[2]};""")
                                        qurey="""SELECT ROUND((((ci.price_at_addition*ci.quantity)*ci.tax_rate)/100+ci.price_at_addition*ci.quantity),2) as "total amount"  FROM CartItems ci JOIN Products p ON ci.product_id = p.product_id JOIN Cart c ON ci.cart_id = c.cart_id WHERE c.user_id = %s;"""
                                        qurey_runner(qurey,(result[2],))
                                        data=cursor.fetchall()
                                        ftotal=0
                                        if data:
                                            for i in data:
                                                for j in i:
                                                    ftotal+=float(j)
                                            print(f"Total Amount : ₹{ftotal}")           
                                    elif choice==2: #remove item from cart
                                        cursor.execute(f"select cart_id from cart where user_id={result[2]};")
                                        # qurey_runner(GET_CARTID_BY_UID_QRY,(result[2],))
                                        cart_id = cursor.fetchone()
                                        if cart_id:
                                            qurey_runner(GET_CARTITEMS_BY_CARTID_QRY,(cart_id,))
                                            rresult = cursor.fetchone()
                                            if rresult:
                                                user_obj.remove_fromcart(result[2])
                                            else:
                                                print("cart is empty")        
                                        else:
                                            print("cart is empty")    
                                    elif choice==3:
                                        cart_id_qurey="select cart_id from cart where user_id=%s;"
                                        qurey_runner(cart_id_qurey,(result[2],))
                                        ccid=cursor.fetchone()
                                        qurey="select * from cartitems where cart_id=%s;"
                                        qurey_runner(qurey,(ccid,))
                                        fresult=cursor.fetchone()
                                        if fresult:
                                            city,pincode,country,district,address,od,da = user_obj.final_checkout(result[2])
                                            user_obj.generate_pdf(result[1],result[2],city,pincode,country,district,address,od[0],da)
                                        else:
                                            print("Your cart is empty,please add items in your cart to checkout")    
                                    elif choice==4:
                                        break
                                    elif choice==5:
                                        user_obj.checkout(result[2])
                                    else:
                                        print(INVALID_INPUT_OPTION)
                                else:
                                    print(INVALID_INPUT_OPTION)  
                            except ValueError:
                                print(INVALID_INPUT_OPTION)                  
                    elif choice==3: #manage account
                        while True:
                            print("1 : View account details")
                            print("2 : Update account details")
                            print("3 : Delete account")
                            print("4 : Back")
                            print("5 : Exit")
                            try:
                                choice=int(input(CHOICE_OPTION))
                                if choice in (1,2,3,4,5):
                                    if choice==1:
                                        display_table(f"""select user_id as "user id",username,password,gender,TO_CHAR(bdate, 'DD-MM-YYYY') AS birthdate,email from users where user_id={result[2]};""")
                                    elif choice==2:
                                        while True:
                                            print("1 : Update username")
                                            print("2 : Update password")
                                            print("3 : Update birth date")
                                            print("4 : Update email")
                                            print("5 : Update gender")
                                            print("6 : Back")
                                            print("7 : Exit")
                                            try:
                                                choice=int(input(CHOICE_OPTION))
                                                if choice in (1,2,3,4,5,6,7):
                                                    if choice==1:
                                                        #update username
                                                        user_obj.update_username(result[2],result[1])
                                                        pass
                                                    elif choice==2:
                                                        #update password
                                                        pass
                                                    elif choice==3:
                                                        #update bdate
                                                        user_obj.update_bdate(result[2],result[1])
                                                        pass
                                                    elif choice==4:
                                                        #update email
                                                        user_obj.update_email(result[2],result[1])
                                                        pass
                                                    elif choice==5:
                                                        #update gender
                                                        user_obj.update_gender(result[2],result[1])
                                                        pass
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
                                    elif choice==3: #delete account
                                        user_obj.remove_user(result[2],result[1])
                                    elif choice==4:
                                        break
                                    elif choice==5:
                                        final_exit()
                                    else:
                                        print(INVALID_INPUT_OPTION)  
                                else:
                                    print(INVALID_INPUT_OPTION)  
                            except ValueError:
                                print(INVALID_INPUT_OPTION)                            
                    elif choice==4: #view wishlist
                        while True:
                            print("1 : View wishlist")
                            print("2 : Remove items from wishlist")
                            print("3 : Back")
                            print("4 : Exit")
                            try:
                                choice=int(input(CHOICE_OPTION))
                                if choice in (1,2,3,4):
                                    if choice==1:
                                        display_table(f"""SELECT p.product_id as "product id", p.name as "product name" FROM wishlistitems wi JOIN Products p ON wi.product_id = p.product_id JOIN wishlist w ON wi.wishlist_id = w.wishlist_id WHERE w.user_id = {result[2]};""")
                                    elif choice==2:
                                        user_obj.remove_from_wishlist(result[2])
                                    elif choice==3:
                                        break
                                    elif choice==4:
                                        final_exit()
                                    else:
                                        print(INVALID_INPUT_OPTION) 
                                else:
                                    print(INVALID_INPUT_OPTION)        
                            except ValueError:
                                print(INVALID_INPUT_OPTION)                   
                    elif choice==5: #order management
                        while True:
                            print("\nOrder management panel")
                            print("1 : View your orders")            
                            print("2 : Back")            
                            print("3 : Exit")
                            try:
                                choice=int(input(CHOICE_OPTION))
                                if choice in (1,2,3):
                                    if choice==1:
                                        qurey_runner(GET_ORDER_ID_BY_UID_QRY,(result[2],))
                                        foid=cursor.fetchone()[0]
                                        if foid:
                                            display_table(f"""SELECT ROW_NUMBER() OVER (PARTITION BY oi.order_id ORDER BY oi.product_id) AS "Si.No", p.name as "product name", p.price AS "price per unit", oi.quantity || ' ' || oi.base_quantity AS quantity, (oi.price * oi.quantity) AS "net amount", o.tax_rate || '%' as "tax rate", o.tax_type, ROUND(((oi.price * oi.quantity) * o.tax_rate) / 100, 2) AS tax_amount, (oi.price * oi.quantity) + ROUND(((oi.price * oi.quantity) * o.tax_rate) / 100, 2) AS "total amount" FROM  orderitems oi JOIN  products p ON oi.product_id = p.product_id  JOIN orders o ON oi.order_id = o.order_id WHERE  oi.order_id = {foid};""")                
                                            qurey="""SELECT SUM(ROUND(((oi.price * oi.quantity) * o.tax_rate) / 100, 2)) OVER (PARTITION BY oi.order_id) AS "total tax amount", SUM((oi.price * oi.quantity) + ROUND(((oi.price * oi.quantity) * o.tax_rate) / 100, 2)) OVER (PARTITION BY oi.order_id) AS "order total amount" FROM  orderitems oi JOIN  products p ON oi.product_id = p.product_id  JOIN orders o ON oi.order_id = o.order_id WHERE  oi.order_id = %s;"""
                                            qurey_runner(qurey,(foid,))
                                            total_tax_ammount,total_amount=cursor.fetchone()

                                            qurey="select TO_CHAR(created_at,'DD Mon YYYY, HH:MI AM') from orders where order_id=%s;"
                                            qurey_runner(qurey,(foid,))
                                            od=cursor.fetchone()[0]

                                            qurey="select TO_CHAR(delivery_date,'DD Mon YYYY, HH:MI AM') from orderitems where order_id=%s;"
                                            qurey_runner(qurey,(foid,))
                                            edod=cursor.fetchone()[0]

                                            qurey="select order_address,order_city,order_district,order_country from orders where order_id=%s;"
                                            qurey_runner(qurey,(foid,))
                                            address,city,district,country=cursor.fetchone()

                                            qurey="select total from orders where order_id=%s;"
                                            qurey_runner(qurey,(foid,))
                                            ap=cursor.fetchone()[0] 

                                            print("\nPament information")
                                            print(f"Amount Paid : {ap}")
                                                    
                                            print("\norder information\n")
                                            print(f"order id : {foid}")
                                            print(f"order date : {od}")
                                            print(f"expected date of delivery : {edod}")

                                            print("\nShipping Address : ")
                                            print(f"{address}")
                                            print(f"{city}, {district}, {country}")

                                            print("\nBilling Address : ")
                                            print(f"{address}")
                                            print(f"{city}, {district}, {country}")

                                        else:
                                            print("you didn't order any product yet")
                                    elif choice==2:
                                        break
                                    elif choice==3:
                                        final_exit()
                                    else:
                                        print(INVALID_INPUT_OPTION)
                                else:
                                    print(INVALID_INPUT_OPTION)        
                            except ValueError:
                                print(INVALID_INPUT_OPTION)                       
                    elif choice==6: #customer support
                        while True:
                            print("\nCustomer Support Panel")
                            print("1 : View support ticket")
                            print("2 : Generate support ticket")
                            print("3 : View support response")
                            print("4 : Back")
                            print("5 : Exit\n")
                            try:
                                choice=int(input(CHOICE_OPTION))
                                if choice in (1,2,3,4,5,6):
                                    if choice==1: #view support ticket
                                        print("\nList of availlable support tickets")
                                        display_table(f"""select ticket_id as "ticket id", subject,message,status,TO_CHAR(created_at,'DD Mon YYYY, HH:MI AM') as "created at",TO_CHAR(updated_at,'DD Mon YYYY, HH:MI AM') as "updated at" from supporttickets where user_id={result[2]} order by ticket_id; """)
                                    elif choice==2: #create support ticket
                                        print("\n")
                                        user_obj.generate_supportticket(result[2])
                                    elif choice==3: #view support responses
                                        display_table(f""" SELECT st.ticket_id, st.subject, st.message AS "ticket message", sr.response_id, sr.message AS "response message", st.status, TO_CHAR(sr.created_at,'DD Mon YYYY, HH:MI AM') AS "response date" FROM  SupportTickets st JOIN SupportResponses sr ON st.ticket_id = sr.ticket_id WHERE st.user_id = {result[2]} ORDER BY  st.ticket_id, sr.created_at;""")   
                                    elif choice==4:
                                        break
                                    elif choice==5:
                                        final_exit()
                                    else:
                                        print(INVALID_INPUT_OPTION)
                                else:
                                    print(INVALID_INPUT_OPTION)    
                            except ValueError:
                                print(INVALID_INPUT_OPTION)        

                    elif choice==7: #logout
                        break
                    elif choice==8: #final exit
                        final_exit()
                else:
                    print(INVALID_INPUT_OPTION)         
            except ValueError:
                print(INVALID_INPUT_OPTION)        
    else:
        print("username or password is incorrect")