import merasql as sql
import analysis as an
import table_ops as to


def initiate():
    sql.db_creation(dbname="humaradb")
    cd = '''
Customer(
Customer_id int(5) primary key, 
Customer_name varchar(30), 
Address varchar(50), 
Phone bigint(13) not null)'''

    sale = '''
Sale(
Sale_id int(10) primary key, 
Customer_id int(5) not null, 
Item_id int(5) not null, 
Quantity int(5), 
Rate_of_sale float(9,2), 
Date date)'''

    item = '''
Item(
Item_id int(5) primary key,
Item_name varchar(30),
Quantity int(7))'''

    pur = '''
Purchase(
Purchase_id int(10) primary key,
Item_id int(5) not null,
Quantity int(7),
Rate_of_purchase float(9,2))'''

    sql.table_creation(struc=cd)
    sql.table_creation(struc=sale)
    sql.table_creation(struc=item)
    sql.table_creation(struc=pur)

    print('''
*************************************
           WELCOME USER 
*************************************

-> For using the application, type the corresponding number
of the menu option you want to choose.''')

    menu1()


# Main Menu
def menu1():
    c1 = input('''\nMain Menu-:
1. Sale
2. Purchase
3. Customer
4. Item
5. View Analysis
6. Exit
Enter choice: ''')

    if c1 == "1":
        menu2("Sale")
    elif c1 == "2":
        menu2("Purchase")
    elif c1 == "3":
        menu2("Customer")
    elif c1 == "4":
        menu2("Item")
    elif c1 == "5":
        menu3()
    elif c1 == "6":
        print("\nThank You")
    else:
        print("\n-> Please enter a valid value!")
        menu1()


# Table Menu
def menu2(table):
    c2 = input(f'''\n{table} Menu-:
1. View records
2. Insert new record
3. Update a record
4. Delete a record
5. Return to main menu
Enter choice: ''')

    if c2 == "1":
        print()
        print(to.view_data(table))
        menu2(table)
    elif c2 == "2":
        to.insert_data(table)
        menu2(table)
    elif c2 == "3":
        to.update_data(table)
        print("-> Data updated successfully.")
        menu2(table)
    elif c2 == "4":
        to.delete_data(table)
        menu2(table)
    elif c2 == "5":
        menu1()
    else:
        print("\n-> Please enter a valid value!")
        menu2(table)


def menu3():
    c3 = input('''\nAnalysis Menu-:
1. Sale per day
2. Sale per item
3. Sale per customer
4. Customer preference
5. Return to main menu
Enter choice: ''')

    if c3 == "1":
        an.g1("Date")
        menu3()
    elif c3 == "2":
        an.g1("Item_id")
        menu3()
    elif c3 == "3":
        an.g1("Customer_id")
        menu3()
    elif c3 == "4":
        an.g2()
        menu3()
    elif c3 == "5":
        menu1()
    else:
        print("\n-> Please enter a valid value!")
        menu3()


try:
    initiate()
except Exception as e:
    print(e)
