from CategoryManagement.category_management import *
from DiscountManagement.discount_management import *
from BillGeneration.generate_bill import *
import indiapins as ip
from Tables.tables import *
from Options.options import *
from Queries.pm_qry import *

class ProductManagement(CategoryManagement,MyPDF,DiscountManagement):
    #view all products
    @staticmethod
    def view_products(qurey):
        cursor.execute(qurey)
        result=cursor.fetchall()
        if result:
            headers = [desc[0] for desc in cursor.description]  # Get column names
            table = tabulate(result, headers, tablefmt='pretty')
            print(table)
        else:
            print("Data Does not exist") 

    #delete product
    @staticmethod
    def remove_product():
        try:
            pid=int(input("Enter the id of the product you want to remove : "))
            cursor.execute(GET_PRODUCTS_BY_PID_QRY,(pid,))
            result=cursor.fetchone()
            if result:
                qurey_runner(DELETE_PRODUCT_BY_PID_QRY,(pid,))
                print("Product removed successfully")
            else:
                print("Product id is not found")    
        except:
            print("id is not valid")    

    #product id cehcker
    @staticmethod
    def check_productid():
        try:
            pid=int(input("Enter product id : "))
            cursor.execute(GET_PRODUCTS_BY_PID_QRY,(pid,))
            result=cursor.fetchone()
            if result:
                return 1,pid
            else:
                print("product id is not found")
                return (-1,0)
        except:
            print("product id is not valid") 
            return (0,0)      

    #product name update
    @staticmethod
    def update_product_name(pid,updated_by):
        pname=input("Enter new product name : ")
        ns=0
        for i in pname:
            if i==" ":
                ns+=1
        if not pname:
            print("product name can't be empty")
        elif ns==len(pname):
            print("product name can't be only spaces")
        elif len(pname)<2 or len(pname) >23:
            print("please enter product name having character between 2 and 23")
        elif not re.match("^[A-Za-z0-9 ]+$", pname):
            print("product name can only contain letters, numbers, and space.")
        else:
            qurey_runner(UPDATE_PRODUCT_NAME__QRY,(pname,updated_by,pid))      
            print("Product name updated successfully")

    #product description update
    @staticmethod
    def update_product_description(pid,updated_by):
        description=input("Enter new product description : ")
        ns=0
        for i in description:
            if i==" ":
                ns+=1
        if not description:
            print("product name can't be empty")
        elif ns==len(description):
            print("product name can't be only spaces")
        elif len(description)<2 or len(description) >30:
            print("please enter product name having character between 2 and 30")
        elif not re.match("^[A-Za-z0-9 ]+$", description):
            print("product name can only contain letters, numbers, and space.")
        else:
            qurey_runner(UPDATE_PRODUCT_DESCRIPTION_QRY,(description,updated_by,pid))      
            print("Product description updated successfully")

    #product stock update
    @staticmethod
    def update_product_stock(product_id,updated_by):
        base_quantity=('gm','kg','ml,','ltr','unit')
        try:
            nstock=int(input("Enter new stock : "))
            while True:
                print("1 : gm")
                print("2 : kg")
                print("3 : ml")
                print("4 : ltr")
                print("5 : unit")
                choice=input("choose base quanitity realted to product from above : ")
                if choice=="1":
                    qurey_runner(UPDATE_PRODUCT_STOCK_QRY,(nstock,updated_by,base_quantity[0],product_id))
                    print("stock updated successfully")
                    break
                elif choice=="2":
                    qurey_runner(UPDATE_PRODUCT_STOCK_QRY,(nstock,updated_by,base_quantity[1],product_id))
                    print("stock updated successfully") 
                    break   
                elif choice=="3":
                    qurey_runner(UPDATE_PRODUCT_STOCK_QRY,(nstock,updated_by,base_quantity[2],product_id))
                    print("stock updated successfully")
                    break    
                elif choice=="4":
                    qurey_runner(UPDATE_PRODUCT_STOCK_QRY,(nstock,updated_by,base_quantity[3],product_id))
                    print("stock updated successfully")
                    break    
                elif choice=="5":
                    qurey_runner(UPDATE_PRODUCT_STOCK_QRY,(nstock,updated_by,base_quantity[4],product_id))
                    print("stock updated successfully")
                    break
                else:
                    print("Invalid input,Please Enter Valid Input")        
        except ValueError:
            print("stock is not valid")    

    #add new product
    def add_product(self):
        pname=0
        description=0
        stock=0
        cid=0
        bq=0
        price=0
        #new product name   
        while True:
            pname=input("Enter new product name : ")
            ns=0
            for i in pname:
                if i==" ":
                    ns+=1
            if not pname:
                print("product name can't be empty")
            elif ns==len(pname):
                print("product name can't be only space") 
            elif len(pname)<2 or len(pname)>23:
                print("product name is between 2 to 23 characters")
            elif not re.match("^[A-Za-z0-9 ]+$",pname):
                print("product name can only contain letters, numbers, and space.")                                     
            else:
                qurey="select * from Products where name=%s"
                qurey_runner(qurey,(pname,))
                result=cursor.fetchone()
                if result:
                    print("another product already exist with this name, please enter new name for the product")
                else:
                    break

        #new product description
        while True:
            description=input("Enter new product description : ")
            ns=0
            for i in description:
                if i==" ":
                    ns+=1
            if not description:
                print("product name can't be empty")
            elif ns==len(description):
                print("product name can't be only spaces")
            elif len(description)<2 or len(description) >30:
                print("please enter product name having character between 2 and 30")
            elif not re.match("^[A-Za-z0-9 ]+$", description):
                print("product name can only contain letters, numbers, and space.")
            else:
                break

        #new product price
        while True:
            try:
                price=int(input("Enter the price for the producct : "))
                break 
            except:
                print("price is not valid")    

        #new product stock in number
        while True:
            try:
                stock=int(input("Enter new stock : "))
                break
            except:
                print("Stock is not valid")    

        #add base quantity for new product
        base_quantity=('gm','kg','ml,','ltr','unit')
        while True:
            print("1 : gm")
            print("2 : kg")
            print("3 : ml")
            print("4 : ltr")
            print("5 : unit")
            choice=input("choose base quanitity realted to product from above : ")
            if choice=="1":
                bq=base_quantity[0]
                break
            elif choice=="2":
                bq=base_quantity[1]
                break   
            elif choice=="3":
                bq=base_quantity[2]
                break    
            elif choice=="4":
                bq=base_quantity[3]
                break    
            elif choice=="5":
                bq=base_quantity[4]
                break
            else:
                print("Invalid input,Please Enter Valid Input")        

        while True:
            try:
                print("\nList of Categories\n")
                display_table(DISPLAY_CATEGORIES_QRY)
                print("\n")
                cid=int(input("Enter Categoryid of product you want to add : "))
                qurey_runner(GET_CATEGORIES_BY_CID_QRY,(cid,))
                result=cursor.fetchone()
                if result:
                    break
                else:
                    print("Category id not found")
                    while True:
                        self.view_categories()
                        print("1 : If you want to add new category")
                        print("2 : Back")
                        print("3 : Exit")
                        choice=input("Choose one option from above : ")
                        if choice=="1":
                            self.add_category()
                            break
                        elif choice=="2":
                            break
                        elif choice=="3":
                            final_exit()
                        else:
                            print("Invalid input,Please Enter Valid Input")       
            except ValueError:
                print("Categoryid is not valid") 
        qurey_runner(ADD_NEW_PRODUCT_QRY,(pname,description,price,stock,bq,cid))
        print("New Product Added Succssfully")
        
    def update_product_categoryid(self,pid,updated_by):
        ncid_check=self.check_categoryid()
        if ncid_check[0]==1:
            qurey_runner(UPDATE_PRODUCT_CATEGORYID_QRY,(ncid_check[1],updated_by,pid))
            print("Category id updated successfully\n")
        elif ncid_check[0]==-1:
            while True:
                self.view_categories()
                print("1 : If you want to add new category")
                print("2 : Back")
                print("3 : Exit")
                choice=input("Choose one option from above : ")
                if choice=="1":
                    self.add_category()
                    break
                elif choice=="2":
                    break
                elif choice=="3":
                    final_exit()
                else:
                    print("Invalid input,Please Enter Valid Input") 
        else:
            pass    
    def update_product_price(self,pid,updated_by):
        try:
            nprice=float(input("Enter new price : "))
            qurey="select price from products where product_id=%s"
            qurey_runner(qurey,(pid,))
            result=cursor.fetchone()
            if result[0]==nprice:
                print("price already same")
            else:
                qurey_runner(UPDATE_PPRICE_QRY,(nprice,updated_by,pid))
                print("Price updated successfully")
        except ValueError:
            print("price is not valid")    

    def cart_creation(self,uid):
        qurey_runner(GET_CART_UID_QRY,(uid,))
        result=cursor.fetchone()
        if result:
            pass
        else:
            qurey_runner(CREATE_CART_UID_QRY,(uid,))
    
    def add_to_cart(self,uid):
       result=self.check_productid()
       if result[0]==1:
            qurey_runner(GET_PSTOCK_BY_PID_QRY,(result[1],))
            ans=cursor.fetchone()
            try:
                quantity=int(input("Enter the quantity : "))
                if ans[0]<quantity:
                    print("out of stock")
                else: 
                    #adding the product to the cart
                    qurey_runner(GET_PBQ_PPRICE_PID_QRY,(result[1],))
                    bq,price=cursor.fetchone()

                    qurey_runner(GET_CARTID_BY_UID_QRY,(uid,))
                    cart_id=cursor.fetchone()
                    
                    #inserting items to the cart
                    qurey_runner(INSERT_ITEMS_INTO_CARTITEMS_QRY,(result[1],cart_id[0],quantity,bq,price))
                    
                    print("product added to cart")   
            except ValueError:
                print("Quantity is not valid")
    def remove_fromcart(self,uid):
        qurey="select cart_id from cart where user_id=%s"
        qurey_runner(qurey,(uid,))
        cid=cursor.fetchone()
        if cid[0]:
            try:
                qurey = "select * from cartitems where cart_id = %s;"
                qurey_runner(qurey,(cid[0],))
                data = cursor.fetchone()
                if data:  
                    pid=int(input("Input product id : "))
                    qurey="select * from cartitems where cart_id=%s"
                    qurey_runner(qurey,(cid[0],))
                    pfound=cursor.fetchone()
                    if pfound:
                        qurey="delete from cartitems where cart_id=%s and product_id=%s"
                        qurey_runner(qurey,(cid[0],pid))
                        print("Product removed from cart")
                    else:
                        print("Product not found")   
                else:
                    print("cart is empty")         
            except ValueError:
                print("Product id is not valid")
        else:
            print("cart is not created")
    def remove_from_wishlist(self,uid):
        qurey_runner(GET_WID_BY_UID_QRY,(uid,))
        cid=cursor.fetchone()
        if cid[0]:
            try:
                pid=int(input("Input product id : "))
                qurey_runner(GET_WITEMS_BY_PID_WID_QRY,(pid,cid[0]))
                pfound=cursor.fetchone()
                if pfound:
                    qurey_runner(DELETE_WITEMS_BY_PID_WID_QRY,(cid[0],pid))
                    print("Product removed from wishlist")
                else:
                    print("Product not found")    
            except ValueError:
                print("Product id is not valid")
        else:
            print("cart is not created")

    def wishlist_creation(self,uid):
        qurey_runner(GET_WLIST_BY_UID_QRY,(uid,))
        result=cursor.fetchone()
        if result:
            pass
        else:
            qurey_runner(CREATE_WISHLIST_BY_UID_QRY,(uid,))                

    def add_to_wishlist(self,uid):
        result=self.check_productid()
        if result[0]==1:
            qurey_runner(GET_WID_BY_UID_QRY,(uid,))
            wishlist_id=cursor.fetchone()
            qurey_runner(INSERT_ITEMS_INTO_WISHLIST_BY_PID_WID_QRY,(result[1],wishlist_id[0]))
            print("product added to wishlist")

    #method for pincode management
    def pincode(self):
        while True:
            pincode=input("Enter the pincode : ")
            if not pincode:
                print("pipncode can't be empty")
            elif len(pincode)>6:
                print("pincode can't contain more than 6 digits") 
            elif ip.matching(pincode)==False:
                print("pincode is not valid")
            else:    
                return pincode,ip.matching(pincode)[0]['Country']
            
    def address(self):
        while True:
            address=input("Enter shipping address : ")
            nns=0
            for i in address:
                if i==" ":
                    nns+=1
            if not address:
                print("address can't empty")
            elif nns==len(address):
                print("address can't be only spaces")    
            elif len(address)>50:
                print("address can't be too long")
            elif  len(address)<2:
                print("address can't be too short")
            else:
                return address

    def city(self):
        while True:
            city=input("Enter name of your city  : ")
            nns=0
            for i in city:
                if i==" ":
                    nns+=1
            if not city:
                print("city can't empty")
            elif nns==len(city):
                print("city can't be only spaces")    
            elif len(city)>50:
                print("city can't be too long")
            elif  len(city)<2:
                print("city can't be too short")
            else:
                return city

    def district(self):
        while True:
            district=input("Enter name of your district  : ")
            nns=0
            for i in district:
                if i==" ":
                    nns+=1
            if not district:
                print("district name can't empty")
            elif nns==len(district):
                print("district name can't be only spaces")    
            elif len(district)>50:
                print("district name can't be too long")
            elif  len(district)<2:
                print("district name can't be too short")
            else:
                return district        

    def final_checkout(self,uid):
        
        address = 0
        pincode = 0
        city = 0
        country = 0
        district = 0
        total = 0
        oid = 0
        order_flag = 0
        new_order_id = 0
        dtotal = 0
        da = 0
        
        #total of the order
        display_table(f"""SELECT p.product_id as "product id",p.name as "product name",'₹' || ci.price_at_addition as "price per unit", ci.quantity || ' ' || ci.base_quantity AS quantity,'₹' || ci.price_at_addition*ci.quantity as "net amount",ROUND(ci.tax_rate,0) || '%' as "tax rate",ci.tax_type as "tax type",'₹' || ROUND(((ci.price_at_addition*ci.quantity)*ci.tax_rate)/100,2) as "tax amount",'₹' || ROUND((((ci.price_at_addition*ci.quantity)*ci.tax_rate)/100+ci.price_at_addition*ci.quantity),2) as "total amount"  FROM CartItems ci JOIN Products p ON ci.product_id = p.product_id JOIN Cart c ON ci.cart_id = c.cart_id WHERE c.user_id = {uid};""")
        qurey="""SELECT ROUND((((ci.price_at_addition*ci.quantity)*ci.tax_rate)/100+ci.price_at_addition*ci.quantity),2) as "total amount"  FROM CartItems ci JOIN Products p ON ci.product_id = p.product_id JOIN Cart c ON ci.cart_id = c.cart_id WHERE c.user_id = %s;"""
        qurey_runner(qurey,(uid,))
        data=cursor.fetchall()
        ftotal=0
        for i in data:
            for j in i:
                ftotal+=float(j)
        print(f"Total Amount : ₹{ftotal}")
        while True:
            if order_flag==1:
                break
            print("1 : UPI")
            print("2 : Debit Card")
            print("3 : Cash on Delivery")
            choice=input("Choose your prefreble payment method : ")
            if choice=="1":
                #upi payment
                pass
            elif choice=="2":
                #debit payment
                pass
            elif choice=="3":
                #cash on delivery      
                dtotal=0  
                dflag=0        
                while True:
                    print("1: Apply Discount Coupan")
                    print("2: Continue")
                    choice=input("Choose one option from the above : ")
                    if choice=="1":
                        discount_coupan=input("Enter discount coupan : ")
                        if not discount_coupan:
                            print("discount coupan can't be empty")
                        elif len(discount_coupan)>20:
                            print("discount coupan can't be too long") 
                        elif len(discount_coupan)<2:
                            print("discount coupan can't bee too short")
                        else:
                            status=self.discount_coupan_checker(discount_coupan)
                            if status==discount_coupan:
                                qurey_runner(GET_DP_BY_DCODE_QRY,(discount_coupan,))
                                dp=cursor.fetchone()[0]
                                dtotal=(ftotal*float(dp))/100
                                print("Discount Coupan applied")
                                print(f"Total Amount without discount : ₹{ftotal}")
                                print(f"Total Amount to be paid : ₹{dtotal}")
                                da=ftotal-dtotal
                                #qurey to increae the number of times the discount coupan is used
                                qurey_runner(UPDATE_DCODE_USAGE_QRY,(discount_coupan,))
                                dflag=1
                                break   
                    elif choice=="2":
                        break
                    else:
                        print("Invalid input")

                address=self.address()
                pincode,country=self.pincode()
                city=self.city()
                district=self.district()
                while True:
                    print("\nCheck all details provided by you")
                    print(f"Shipping Address : {address}")        
                    print(f"Pincode : {pincode}")        
                    print(f"City : {city}")        
                    print(f"District : {district}")        
                    print(f"Country : {country}") 
                    if dflag==1:
                        print(f"Amount to be Paid : {dtotal}\n")
                    else:
                        print(f"Amount to be Paid : {ftotal}\n")    
                    choice=input("Press 1 to place your order : ")
                    if choice=="1":
                        print("Please Wait...")
                        for i in range(1,150):
                            pass
                        qurey_runner(GET_CARTID_BY_UID_QRY,(uid,))
                        cid=cursor.fetchone() 

                        # Step 1: Insert new order and get order_id
                        if dflag==1:   
                            qurey_runner(INSERT_INTO_ORDER_GET_OID_QRY, (uid, 'pending', dtotal, address, city, pincode, country, district))
                        else:
                            qurey_runner(INSERT_INTO_ORDER_GET_OID_QRY, (uid, 'pending', ftotal, address, city, pincode, country, district))
                        new_order_id = cursor.fetchone()[0]

                        #getting orderd at date
                        qurey=f"select TO_CHAR(created_at,'DD-MM-YYYY') from orders where order_id={new_order_id};"
                        cursor.execute(qurey)
                        od=cursor.fetchone() 

                        # Step 2: Move items from cartitems to orderitems
                        qurey_runner(MOVE_ITEMS_FROM_CART_TO_ORDERITEMS_QRY, (new_order_id, cid))

                        # removing items from the stock that are ordered
                        rqurey=f"UPDATE products SET stock = stock - oi.quantity FROM orderitems oi WHERE oi.product_id = products.product_id AND oi.order_id = {new_order_id};"
                        cursor.execute(rqurey)
                        db_cnn.commit()

                        # Step 3: Delete items from cartitems
                        qurey_runner(DELETE_ITEMS_FROM_CART_QRY, (cid,)) 
                        print("Your Order has been placed Successfully")       
                        order_flag=1
                        return city,pincode,country,district,address,od,da
                    else:
                        print("Invalid input")  
            else:
                print("Invalid input")