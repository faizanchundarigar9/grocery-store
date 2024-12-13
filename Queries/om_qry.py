DISPLAY_ORDERS_QRY ="""SELECT order_id as "order id",user_id as "user id", total,status, TO_CHAR(created_at, 'DD Mon YYYY, HH:MI AM') AS "created at",TO_CHAR(updated_at, 'DD Mon YYYY, HH:MI AM') AS "updated at", updated_by as "updated by" FROM Orders;"""
GET_ORDERS_BY_OID_QRY = "select * from orders where order_id=%s;"
REMOVE_ORDER_BY_OID_QRY = "delete from orders where order_id=%s;"
UPDATE_ORDER_STATUS_QRY = "update orders set updated_by=%s,updated_at=current_timestamp,status=%s where order_id=%s;"
UPDATE_ORDER_TOTAL_QRY = "update orders set total=%s,updated_by=%s,updated_at=current_timestamp where order_id=%s;"
GET_ORDER_ID_BY_UID_QRY = "select order_id from orders where user_id=%s order by order_id desc;"