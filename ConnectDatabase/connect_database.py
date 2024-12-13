import psycopg2
from psycopg2 import sql

# Method used for making connection with databse
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="GS",
            user="root",
            password="Faizan9@4518",
            host="localhost",
            port="5432"  # Default PostgreSQL port
        )
        # print("Database connection successful")
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# creating connection with data base createing a cursor to run qureis   
db_cnn = connect_to_db()
if db_cnn:
    cursor=db_cnn.cursor()
cf=0

# creating qurey runner for running quries
def qurey_runner(qurey,params):
    cursor.execute(qurey,params)
    db_cnn.commit()  
