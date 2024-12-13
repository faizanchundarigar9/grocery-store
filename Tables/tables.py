from ConnectDatabase.connect_database import *
from tabulate import tabulate

def display_table(qurey):
    cursor.execute(qurey)
    result=cursor.fetchall()
    if result:
        headers = [desc[0] for desc in cursor.description]  # Get column names
        table = tabulate(result, headers, tablefmt='pretty')
        print(table)
    else:
        print("no data found")