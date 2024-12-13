
# quaries for the authentication (login for admin and user)
AUTHENTICATION_QRY = "SELECT user_id FROM USERS WHERE USERNAME=%s and password=%s and role=%s;"

# --------------------------- product management quaries --------------------------------------

GET_PRODUCTS_BY_PID_QRY = "select * from Products where product_id = %s;"
GET_PRODUCTS_BY_PNAME_QRY = "select * from Products where name=%s;"
UPDATE_PRODUCT_NAME__QRY = "update products set name=%s,updated_at=current_timestamp,updated_by=%s where product_id=%s;"
UPDATE_PRODUCT_DESCRIPTION_QRY = "update products set description=%s,updated_at=current_timestamp,updated_by=%s where product_id=%s;"
UPDATE_PRODUCT_STOCK_QRY = "update Products set stock=%s,updated_at=current_timestamp,updated_by=%s,base_quantity=%s where product_id=%s;"
PRODUCT_CATEGORY_CEHCKER_QRY = "select * from categories where category_id=%s;"
ADD_NEW_PRODUCT_QRY = "INSERT INTO Products (name,description,price,stock,base_quantity,category_id) values (%s,%s,%s,%s,%s,%s);"
UPDATE_PRODUCT_CATEGORYID_QRY = "UPDATE Products set category_id=%s,updated_by=%s,updated_at=current_timestamp where product_id=%s;"
GET_PPRICE_PID_QRY = "select price from products where product_id=%s;"
UPDATE_PPRICE_QRY = "update products set price=%s,updated_at=current_timestamp,updated_by=%s where product_id=%s;"
GET_CART_UID_QRY = "select * from cart where user_id=%s;"
CREATE_CART_UID_QRY = "insert into cart (user_id) values (%s);"
GET_PSTOCK_BY_PID_QRY = "select stock from products where product_id=%s;"
GET_PBQ_PPRICE_PID_QRY = "select base_quantity,price from products where product_id=%s;"
GET_CARTID_BY_UID_QRY = "select cart_id from cart where user_id=%s;"
INSERT_ITEMS_INTO_CARTITEMS_QRY = "insert into cartitems (product_id,cart_id,quantity,base_quantity,price_at_addition) values (%s,%s,%s,%s,%s);"
GET_CARTITEMS_BY_PID_CARTID_QRY = "select * from cartitems where cart_id=%s and product_id=%s ;"
DELETE_CARTITEM_BY_PID_CARTID_QRY = "delete from cartitems where cart_id=%s and product_id=%s;"  
GET_WID_BY_UID_QRY = "select wishlist_id from wishlist where user_id=%s;"
GET_WITEMS_BY_PID_WID_QRY = "select * from wishlistitems where product_id=%s and wishlist_id=%s;"
DELETE_WITEMS_BY_PID_WID_QRY = "delete from wishlistitems where wishlist_id=%s and product_id=%s;"
GET_WLIST_BY_UID_QRY = "select * from wishlist where user_id=%s;"
CREATE_WISHLIST_BY_UID_QRY = "insert into wishlist (user_id) values (%s);"
INSERT_ITEMS_INTO_WISHLIST_BY_PID_WID_QRY = "insert into wishlistitems (product_id,wishlist_id) values (%s,%s);"
INSERT_INTO_ORDER_GET_OID_QRY = """ INSERT INTO orders (user_id, status, total, order_address, order_city, order_pincode, order_country, order_district) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING order_id;"""
MOVE_ITEMS_FROM_CART_TO_ORDERITEMS_QRY = """ INSERT INTO orderitems (order_id, product_id, quantity, base_quantity, price) SELECT %s, product_id, quantity, base_quantity, price_at_addition FROM cartitems WHERE cart_id = %s;"""
DELETE_ITEMS_FROM_CART_QRY = """DELETE FROM cartitems WHERE cart_id = %s;"""
DELETE_PRODUCT_BY_PID_QRY = "DELETE FROM Products WHERE product_id=%s;"
GET_CATEGORIES_BY_CID_QRY = "select * from categories where category_id=%s;"
GET_DP_BY_DCODE_QRY = "select discount_percent from discounts where code=%s;"
UPDATE_DCODE_USAGE_QRY = "update discounts set number_of_times_used=number_of_times_used+1 where code=%s;"


# ---------------- USER MANAGEMENT QUARIES -----------------

DISPLAY_USERS_QRY = """SELECT user_id as id, username, gender,email, role, TO_CHAR(bdate, 'DD-MM-YYYY') AS birthdate, TO_CHAR(created_at, 'DD Mon YYYY, HH:MI AM') AS "created at",TO_CHAR(updated_at, 'DD Mon YYYY, HH:MI AM') AS "updated at", updated_by as "updated by"FROM Users order by user_id;""" 
GET_USER_BY_UID_QRY = "select * from users where user_id=%s;"
UPDATE_USERNAME_BY_UID_QRY = "UPDATE USERS SET USERNAME=%s,updated_by=%s,updated_at=current_timestamp where user_id=%s;"
UPDATE_USEREMAIL_BY_UID_QRY = "UPDATE USERS SET email=%s,updated_by=%s,updated_at=current_timestamp where user_id=%s;"
UPDATE_USER_GENDER_BY_UID_QRY = "UPDATE USERS SET GENDER=%s,updated_by=%s,updated_at=current_timestamp where user_id=%s;"
GET_GENDER_BY_UID_QRY = "select gender from users where user_id=%s;"
UPDATE_USER_BDATE_BY_UID_QRY = "UPDATE USERS SET bdate=TO_DATE(%s,'DD-MM-YYYY'),updated_by=%s,updated_at=current_timestamp where user_id=%s;"
GET_UID_BY_UNAME_QRY = "select user_id from users where username=%s;"
DELETE_USER_BY_UID_QRY = "DELETE FROM USERS WHERE user_id=%s;"
INSERT_NEW_USER_QRY = "INSERT INTO USERS (username,password,role,email,gender,bdate) values (%s,%s,%s,%s,%s,%s);"
DIPLAY_USER_REGISTRATION_REQUESTS_QRY = "select * from userregistrationrequests;"
GET_USER_FROM_URR_BY_REQUEST_ID_QRY = "select * from userregistrationrequests where request_id=%s;"
UPDATE_UREGISTRATION_REQUEST_QRY = "UPDATE UserRegistrationRequests SET status = %s WHERE request_id = %s;"
MOVE_USER_FRROM_RR_TO_USERS_QRY = "INSERT INTO Users (username, password, email, role, bdate, gender) SELECT username, password, email, role,bdate, gender FROM UserRegistrationRequests WHERE request_id = %s;"

# ----------------------- USERS QURIES ----------------------

DISPLAY_ACTIVE_CATEGORIES_QRY = """select category_id as id,name,description FROM CATEGORIES where status='active' order by category_id;"""
DISPLAY_PRODUCT_BY_CID_QRY = f"""SELECT p.product_id as "product id", p.name AS "product name", p.description, p.price || '₹' price, CONCAT(p.stock,' ',p.base_quantity) as stock, c.name AS "category name" FROM Products p JOIN Categories c ON p.category_id = c.category_id where c.category_id=%s;"""
GET_CARTITEMS_BY_CARTID_QRY = "select * from cartitems where cart_id=%s;"
GET_USERNAME_QRY = "select * from users where username=%s;"
GET_CARTID_BY_UID_QRY ="select cart_id from cart where user_id=%s"

# ---------------------- DISCOUNT MANAGEMENT QUARIES -------------------------

GET_DISCOUNTS_BY_DID_QRY = "select * from discounts where discount_id=%s;"
GET_DISCOUNTS_BY_DCODE_QRY = "select * from discounts where code=%s;"
UPDATE_DCODE_QRY = "UPDATE Discounts set code=%s,updated_by=%s,updated_at=current_timestamp where discount_id=%s;"
UPDATE_DCODE_DESCRIPTION_QRY = "UPDATE Discounts set description=%s,updated_by=%s,updated_at=current_timestamp where discount_id=%s;"
UPDATE_DCODE_PERCENTAGE_QRY = "UPDATE Discounts set discount_percentage=%s,updated_by=%s,updated_at=current_timestamp where discount_id=%s;"
GET_DCODE_VALIDTO_QRY = "select valid_to from Discounts where discount_id=%s;"
GET_DCODE_VALIDFROM_QRY = "select valid_from from Discounts where discount_id=%s;"
UPDATE_DCODE_VALID_FROM_QRY = "update Discounts set valid_from=%s,updated_by=%s,updated_at=current_timestamp where discount_id=%s;"
UPDATE_DCODE_VALID_TO_QRY = "update Discounts set valid_to=%s,updated_by=%s,updated_at=current_timestamp where discount_id=%s;"
UPDATE_DCODE_STATUS_QRY = "update Discounts set status=%s,updated_at=current_timestamp,updated_by=%s where discount_id=%s;"
GET_DCODE_STATUS_BY_DID_QRY = "select status from Discounts where discount_id=%s;"
GET_DCODE_STATUS_BY_DCODE_QRY = "select status from Discounts where code=%s;"
UPDATE_DCODE_MAXUSAGE_QRY = "UPDATE Discounts set max_usage=%s,updated_by=%s,updated_at=current_timestamp where discount_id=%s;"
DELETE_DCODE_QRY = "delete from discounts where discount_id=%s;"
GET_VALIDATE_DCODE_QRY = "SELECT * FROM discounts WHERE code = %s AND NOW() BETWEEN valid_from AND valid_to;"
GET_DCODE_MAXUSAGE_VALIDATE_QRY = "select * from discounts where code=%s and max_usage>0;"
ADD_NEW_DCODE_QRY = "INSERT INTO Discounts (code,description,discount_percent,valid_from,valid_to,status,max_usage) values (%s,%s,%s,%s,%s,%s,%s);"

# -------------------------- order management quaries -----------------------------

DISPLAY_ORDERS_QRY ="""SELECT order_id as "order id",user_id as "user id", total,status, TO_CHAR(created_at, 'DD Mon YYYY, HH:MI AM') AS "created at",TO_CHAR(updated_at, 'DD Mon YYYY, HH:MI AM') AS "updated at", updated_by as "updated by" FROM Orders;"""
GET_ORDERS_BY_OID_QRY = "select * from orders where order_id=%s;"
REMOVE_ORDER_BY_OID_QRY = "delete from orders where order_id=%s;"
UPDATE_ORDER_STATUS_QRY = "update orders set updated_by=%s,updated_at=current_timestamp,status=%s;"
UPDATE_ORDER_TOTAL_QRY = "update orders set total=%s,updated_by=%s,updated_at=current_timestamp where order_id=%s;"
GET_ORDER_ID_BY_UID_QRY = "select order_id from orders where user_id=%s order by order_id desc;"

# --------------------------- customer support management quaries -----------------------------

VIEW_SUPPORT_TICKETS_QRY = """select ticket_id as "ticket id",user_id as "user id",subject,message,status,TO_CHAR(created_at,'DD Mon YYYY, HH:MI AM') as "created at",TO_CHAR(updated_at,'DD Mon YYYY, HH:MI AM') as "updated at",updated_by as "updated by" from supporttickets;"""
VIEW_SUPPORT_RESPONSES_QRY = """select response_id as "response id",ticket_id as "ticket id", message,TO_CHAR(created_at,'DD Mon YYYY, HH:MI AM') as "created at",TO_CHAR(updated_at,'DD Mon YYYY, HH:MI AM') as "updated at",updated_by as "updated by" from supportresponses;"""
UPDATE_ST_STATUS_QRY = "update supporttickets set status=%s,updated_at=current_timestamp,updated_by=%s where ticket_id=%s;"
GET_STS_BY_TID_QRY = "select * from supporttickets where ticket_id=%s;"
GET_SR_BY_RID_QRY = "select * from supportresponses where response_id=%s;"
UPDATE_SR_MESSAGE_QRY = "update supportresponses set message=%s,updated_at=current_timestamp,updated_by=%s where response_id=%s;"
INSERT_SR_QRY = "INSERT INTO SUPPORTRESPONSES (message,ticket_id) values (%s,%s);"
INSERT_ST_QRY = "insert into supporttickets (subject,message,user_id,status) values (%s,%s,%s,'open');" 
GET_ST_STATUS_BY_TID_QRY = "select status from supporttickets where ticket_id=%s"

# ----------------------------- category management quaries --------------------------------------

VIEW_CATEGORIES_QRY = """select category_id as id,name,description,status,TO_CHAR(created_at, 'DD Mon YYYY, HH:MI AM') AS "created at",TO_CHAR(updated_at, 'DD Mon YYYY, HH:MI AM') AS "updated at", updated_by as "updated by" FROM CATEGORIES;"""
UPDATE_CATEGORY_NAME_QRY = "UPDATE CATEGORIES SET NAME=%s,UPDATED_AT=CURRENT_TIMESTAMP,UPDATED_BY =%s where category_id=%s"
UPDATE_CATEGORY_DESCRIPTION_QRY = "UPDATE CATEGORIES SET description=%s,UPDATED_AT=CURRENT_TIMESTAMP,UPDATED_BY =%s where category_id=%s;"
GET_CATEGORIES_BY_CID_QRY = "select * from categories where category_id=%s;"
DELETE_CATEGORY_BY_CID_QRY = "delete from Categories where category_id=%s;"
ADD_NEW_CATEGORY_QRY = "INSERT INTO Categories (NAME,DESCRIPTION) VALUES (%s,%s);"
