from ConnectDatabase.connect_database import *
from tabulate import tabulate
import re
from Queries.cm_qry import *

def update_category_status():
        # Select all categories
    cursor.execute("SELECT category_id FROM Categories")
    categories = cursor.fetchall()
        
    for category in categories:
        category_id = category[0]
            
            # Count the number of products in the category
        cursor.execute("SELECT COUNT(*) FROM Products WHERE category_id = %s", (category_id,))
        product_count = cursor.fetchone()[0]
            
            # Update the status based on the product count
        if product_count > 0:
            qurey_runner("UPDATE Categories SET status = 'active' WHERE category_id = %s", (category_id,))
        else:
            qurey_runner("UPDATE Categories SET status = 'inactive' WHERE category_id = %s", (category_id,))

class CategoryManagement():
    
    @staticmethod
    #update category name
    def update_category_name(category_id,updated_by):
        category_name=input("Enter new category name : ")
        ns=0
        for i in category_name:
            if i==" ":
                ns+=1        
        if not category_name:
            print("category name can't be empty")
        elif len(category_name)==ns:
            print("category name can't be only space") 
        elif len(category_name)<3 or len(category_name)>20:
            print("category name is too long,please add category name having more than 3 and less than 20 characters")     
        elif not re.match("^[A-Za-z0-9 ]+$", category_name):
                print("category name can only contain letters, numbers, and space\n")    
        else:
            qurey_runner(UPDATE_CATEGORY_NAME_QRY,(category_name,updated_by,category_id))
            print("Category Name Updated Successfully")

    @staticmethod
    #update category description
    def update_category_description(category_id,updated_by):
        description=input("Enter new description : ")
        ns=0
        for i in description:
            if i==" ":
                ns+=1

        if not description:
            print("description can't be empty")
        elif len(description)==ns:
            print("description can't be only spaces") 
        elif len(description)<2 or len(description)>30:
            print("please add description having more then equal to 2 and less than 30 characters") 
        elif not re.match("^[A-Za-z0-9 ]+$", description):
            print("category description can only contain letters, numbers, and space\n")                     
        else:
            qurey_runner(UPDATE_CATEGORY_DESCRIPTION_QRY,(description,updated_by,category_id))
            print("Category Description Updated Successfully")   
                         
    #category id checker
    def check_categoryid(self):
        try:
            category_id=int(input("Enter CategoryId : "))
            qurey_runner(GET_CATEGORIES_BY_CID_QRY,(category_id,))
            result=cursor.fetchone()
            if result:
                return 1,category_id
            else:
                print("Categoryid not found")
                return (-1,0)
        except ValueError:
            print("Categoryid is not valid") 
            return (0,0)  

    #category remove
    def remove_category(self):
        result=self.check_categoryid()
        if result[0]==1:
            qurey_runner(DELETE_CATEGORY_BY_CID_QRY,(result[1],))
            print("Category Removed Successfully")

    @staticmethod
    def add_category(): #add new category 
        category_name=''
        description=''
        while True:#category name with validation
            category_name=input("Enter category name : ")
            ns=0
            for i in category_name:
                if i==" ":
                    ns+=1        
            if not category_name:
                print("category name can't be empty")
            elif len(category_name)==ns:
                print("category name can't be only space") 
            elif len(category_name)<3 or len(category_name)>20:
                print("category name is too long,please add category name having more than 3 and less than 20 characters")
            elif not re.match("^[A-Za-z0-9 ]+$", category_name):
                print("category name can only contain letters, numbers, and space\n")
            else:
                break

        while True: #category description with validation    
            description=input("Enter new description : ")
            ns=0
            for i in description:
                if i==" ":
                    ns+=1
            if not description:
                print("description can't be empty")
            elif len(description)==ns:
                print("description can't be only spaces")
            elif len(description)<2 or len(description)>30:
                print("please add description having more then equal to 2 and less than 30 characters")
            elif not re.match("^[A-Za-z0-9 ]+$", description):
                print("category description can only contain letters, numbers, and space\n")
            else:
                break
              
        qurey_runner(ADD_NEW_CATEGORY_QRY,(category_name,description))   
        print("New Category Added Successfully")